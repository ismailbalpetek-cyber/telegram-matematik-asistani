import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ========================
# ORTAM DEĞİŞKENLERİ
# ========================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if not BOT_TOKEN or not GOOGLE_API_KEY:
    raise RuntimeError("BOT_TOKEN veya GOOGLE_API_KEY eksik")

# ========================
# GEMINI AYARI (DOĞRU MODEL)
# ========================
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""
Sen bir matematik öğretmenisin.
Gelen soruya BENZER 2 adet beceri temelli matematik sorusu üret.
Her soru:
- 4 şıklı olsun
- Tek doğru cevabı olsun
- Çözümü adım adım yaz
- Türkçe ve profesyonel olsun
"""
)

# ========================
# PDF OLUŞTURMA
# ========================
def pdf_olustur(metin):
    dosya = "sorular.pdf"
    c = canvas.Canvas(dosya, pagesize=A4)
    text = c.beginText(40, 800)

    for satir in metin.split("\n"):
        text.textLine(satir)

    c.drawText(text)
    c.showPage()
    c.save()
    return dosya

# ========================
# TELEGRAM MESAJI
# ========================
async def mesaj_al(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("✍️ Düşünüyorum...")

        prompt = f"""
Aşağıdaki matematik sorusuna benzer 2 adet yeni soru üret.

SORU:
{update.message.text}
"""

        response = model.generate_content(prompt)
        sonuc = response.text

        pdf = pdf_olustur(sonuc)

        await update.message.reply_document(
            document=open(pdf, "rb"),
            filename="Matematik_Sorulari.pdf"
        )

    except Exception as e:
        await update.message.reply_text(f"❌ Hata oluştu:\n{str(e)}")

# ========================
# BOT BAŞLAT
# ========================
logging.basicConfig(level=logging.INFO)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mesaj_al))

print("🤖 Bot çalışıyor (Gemini 2.5 Flash)")
app.run_polling()
