import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
RENDER_URL = os.environ.get("RENDER_URL")  # https://xxxxx.onrender.com

async def mesaj_yakala(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Mesaj alındı ✅\n\nGönderdiğin içerik:\n{update.message.text}"
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, mesaj_yakala)
    )

    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        url_path=BOT_TOKEN,
        webhook_url=f"{RENDER_URL}/{BOT_TOKEN}",
    )

if __name__ == "__main__":
    main()
