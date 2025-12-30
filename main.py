import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters
)
from flask import Flask, request

BOT_TOKEN = os.environ.get("BOT_TOKEN")

app_flask = Flask(__name__)

async def mesaj_yakala(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Mesaj alındı ✅\n\nGönderdiğin içerik:\n{update.message.text}"
    )

@app_flask.route(f"/{BOT_TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok"

@app_flask.route("/", methods=["GET"])
def index():
    return "Bot çalışıyor"

application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mesaj_yakala))

if __name__ == "__main__":
    app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
