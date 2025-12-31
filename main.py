import os
import base64
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# ===============================
# ORTAM DEĞİŞKENLERİ
# ===============================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# ===============================
# GEMINI AYARI (GÜNCEL MODEL)
# ===============================
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# ===============================
# MESAJ YAKALAYICI
# ===============================
async def mesaj_yakala(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # -------- METİN --------
        if update.message.text:
            soru = update.message.text

        # -------- FOTOĞRAF --------
        elif update.message.photo:
            photo = update.message.photo[-1]
            file = await photo.get_file()
            image_bytes = await file.download_as_bytearray()

            image_base64 = base64.b64encode(image_bytes).decode("utf-8")

            response = model.generate_content([
                "Bu görseldeki matematik sorusunu aynen yazıya dök. "
                "Açıklama yapma.",
                {
                    "mime_type": "image/png",
                    "data": image_base64
                }
            ])

            soru = response.text.strip()

        else:
            await update.message.reply_text("❗ Metin veya fotoğraf gönder.")
            return

        await update.message.reply_text(
            "📘 Soru alındı:\n\n" + soru
        )

    except Exception as e:
        await update.message.reply_text(
            "❌ Hata oluştu:\n" + str(e)
        )

# ===============================
# BOTU ÇALIŞTIR
# ===============================
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, mesaj_yakala))
app.run_polling()
