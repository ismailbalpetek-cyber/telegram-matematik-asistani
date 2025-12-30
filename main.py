import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def mesaj_yakala(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text:
        soru = update.message.text

    elif update.message.photo:
        photo = update.message.photo[-1]
        file = await photo.get_file()
        image_bytes = await file.download_as_bytearray()

        response = model.generate_content([
            "Bu görseldeki matematik sorusunu aynen yazıya dök.",
            image_bytes
        ])
        soru = response.text

    else:
        return

    await update.message.reply_text(
        "📘 Soru alındı:\n\n" + soru
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, mesaj_yakala))
app.run_polling()
