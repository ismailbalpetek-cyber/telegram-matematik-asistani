import os
print("BOT_TOKEN var mı:", bool(os.environ.get("BOT_TOKEN")))
print("GOOGLE_API_KEY var mı:", bool(os.environ.get("GOOGLE_API_KEY")))
import base64
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# ===============================
# ORTAM DEĞİŞKENLERİ
# ===============================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN bulunamadı")

if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY bulunamadı")

# ===============================
# GEMINI AYARI
# ===============================
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ===============================
# MESAJ YAKALAYICI
# ===============================
async def mesaj_yakala(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # -------- METİN GELİRSE --------
        if update.message.text:
            soru = update.message.text

        # -------- FOTOĞRAF GELİRSE --------
        elif update.message.photo:
            photo = update.message.photo[-1]
            file = await photo.get_file()
            image_bytes = await file.download_as_bytearray()

            image_base64 = base64.b64encode(image_bytes).decode("utf-8")

            response = model.generate_content([
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": (
                                "Bu görseldeki matematik sorusunu "
                                "aynen yazıya dök. Açıklama yapma, "
                                "sadece soruyu yaz."
                            )
                        },
                        {
                            "inline_data": {
                                "mime_type": "image/png",
                                "data": image_base64
                            }
                        }
                    ]
                }
            ])

            soru = response.text.strip()

        else:
            await update.message.reply_text("❗ Metin veya fotoğraf gönder.")
            return

        # -------- SONUÇ --------
        await update.message.reply_text(
            "📘 Soru alındı:\n\n" + soru
        )

    except Exception as e:
        await update.message.reply_text(
            "❌ Bir hata oluştu:\n\n" + str(e)
        )

# ===============================
# BOTU ÇALIŞTIR
# ===============================
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, mesaj_yakala))
app.run_polling()
