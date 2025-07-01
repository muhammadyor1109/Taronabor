import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# 🔐 ADMIN ID (o'zingizni Telegram ID'ingiz)
ADMIN_ID = 5914262935

# 🎵 Tarona papkasi
AUDIO_FOLDER = 'audio'
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# 🎹 Tugmalar
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("🎵 Tarona")],
        [KeyboardButton("🔐 Admin panel")]
    ],
    resize_keyboard=True
)

# /start buyrug‘i
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Xush kelibsiz! Quyidagi tugmalardan foydalaning.",
        reply_markup=main_keyboard
    )

# 🎵 Tarona tugmasi
async def handle_tarona(update: Update, context: ContextTypes.DEFAULT_TYPE):
    files = os.listdir(AUDIO_FOLDER)
    if not files:
        await update.message.reply_text("🚫 Hozircha hech qanday tarona mavjud emas.")
        return
    latest = sorted(files)[-1]
    with open(f"{AUDIO_FOLDER}/{latest}", 'rb') as audio_file:
        await update.message.reply_audio(audio=audio_file, title=latest)

# 🔐 Admin panel tugmasi
async def handle_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Siz admin emassiz.")
        return
    await update.message.reply_text("🔐 Admin paneliga xush kelibsiz!\nTarona yuboring — saqlanadi.")

# Admin audio yuboradi
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Siz audio yubora olmaysiz.")
        return

    audio = update.message.audio or update.message.voice or update.message.document
    if not audio:
        await update.message.reply_text("🚫 Audio topilmadi.")
        return

    file = await context.bot.get_file(audio.file_id)
    filename = f"{audio.file_unique_id}.mp3"
    filepath = os.path.join(AUDIO_FOLDER, filename)
    await file.download_to_drive(filepath)

    await update.message.reply_text(f"✅ Tarona saqlandi: {filename}")

# 🔄 Botni ishga tushirish
if name == 'main':
    TOKEN = "7944639897:AAHrcHqpVUAP6H65goYpJIrkwDzYhbcbJTc"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^🎵 Tarona$"), handle_tarona))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^🔐 Admin panel$"), handle_admin))
    app.add_handler(MessageHandler(filters.AUDIO | filters.Document.AUDIO, handle_audio))

    print("✅ Bot ishga tushdi...")
    app.run_polling()