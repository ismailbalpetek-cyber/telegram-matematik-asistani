import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from google import genai
from PIL import Image
import io

# ===============================
# ORTAM DEĞİŞKENLERİ
# ===============================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if not BOT_TOKEN or not GOOGLE_API_KEY:
    raise RuntimeError("BOT_TOKEN veya GOOGLE_API_KEY eksik")

# ===============================
# GEMINI CLIENT
# ===============================
client = genai.Client(api_key=GOOGLE_API_KEY)

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

            image = Image.open(io.BytesIO(image_bytes))

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    "Bu görseldeki matematik sorusunu aynen yazıya dök. Açıklama yapma.",
                    image
                ]
            )

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
