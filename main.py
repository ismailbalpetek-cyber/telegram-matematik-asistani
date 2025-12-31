import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from google import genai
from google.genai import types
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

# ========================
# ORTAM DEĞİŞKENLERİ
# ========================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if not BOT_TOKEN or not GOOGLE_API_KEY:
    raise RuntimeError("BOT_TOKEN veya GOOGLE_API_KEY eksik")

# ========================
# GEMINI AYARI (YENİ API)
# ========================
client = genai.Client(api_key=GOOGLE_API_KEY)

SYSTEM_INSTRUCTION = """
Sen bir matematik öğretmenisin.
Gelen soruya BENZER 2 adet beceri temelli matematik sorusu üret.
Her soru:
- 4 şıklı olsun
- Tek doğru cevabı olsun
- Çözümü adım adım yaz
- Türkçe ve profesyonel olsun
"""

# ========================
# PDF OLUŞTURMA
# ========================
def pdf_olustur(metin):
    dosya = "sorular.pdf"
    c = canvas.Canvas(dosya, pagesize=A4)
    width, height = A4
    
    # Başlangıç pozisyonu
    y = height - 2*cm
    x = 2*cm
    max_width = width - 4*cm
    
    c.setFont("Helvetica", 11)
    
    for satir in metin.split("\n"):
        if y < 2*cm:  # Sayfa sonu kontrolü
            c.showPage()
            c.setFont("Helvetica", 11)
            y = height - 2*cm
        
        # Uzun satırları böl
        if len(satir) > 80:
            words = satir.split()
            current_line = ""
            for word in words:
                test_line = current_line + " " + word if current_line else word
                if len(test_line) <= 80:
                    current_line = test_line
                else:
                    c.drawString(x, y, current_line)
                    y -= 14
                    current_line = word
            if current_line:
                c.drawString(x, y, current_line)
                y -= 14
        else:
            c.drawString(x, y, satir)
            y -= 14
    
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

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.7,
                max_output_tokens=2048
            )
        )
        
        sonuc = response.text

        pdf = pdf_olustur(sonuc)

        with open(pdf, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename="Matematik_Sorulari.pdf"
            )

    except Exception as e:
        logging.error(f"Hata: {e}")
        await update.message.reply_text(f"❌ Hata oluştu:\n{str(e)}")

# ========================
# HATA YÖNETİCİSİ
# ========================
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Update {update} caused error {context.error}")

# ========================
# BOT BAŞLAT
# ========================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mesaj_al))
app.add_error_handler(error_handler)

print("🤖 Bot çalışıyor (Gemini 2.0 Flash)")
app.run_polling(drop_pending_updates=True)
