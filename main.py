from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8545319991:AAGMxJ4L_iDZgdYu3yLaCGpncNiHpj7ipRE"

async def mesaj_yakala(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gelen_mesaj = update.message.text
    await update.message.reply_text(
        f"Mesaj alındı ✅\n\nGönderdiğin içerik:\n{gelen_mesaj}"
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mesaj_yakala))

app.run_polling()
