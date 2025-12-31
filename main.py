import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# ==============================
# ENV KONTROLLERİ
# ==============================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ZAI_API_KEY = os.environ.get("ZAI_API_KEY")

if not BOT_TOKEN or not ZAI_API_KEY:
    raise RuntimeError("BOT_TOKEN veya ZAI_API_KEY eksik")

# ==============================
# Z.AI API AYARLARI
# ==============================
ZAI_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
MODEL_NAME = "glm-4-flash"   # En stabil ve ücretsiz modele en yakın

HEADERS = {
    "Authorization": f"Bearer {ZAI_API_KEY}",
    "Content-Type": "application/json"
}

# ==============================
# Z.AI SORU CEVAPLAMA FONKSİYONU
# ==============================
def zai_cevap_uret(soru: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": soru
            }
        ]
    }

    r = requests.post(ZAI_URL, headers=HEADERS, json=payload, timeout=30)

    if r.status_code != 200:
        return f"❌ API Hatası ({r.status_code})\n{r.text}"

    data = r.json()

    # ✅ Z.AI GERÇEK CEVAP OKUMA
    try:
        return data["data"]["content"]
    except Exception:
        return f"❌ Cevap formatı beklenmedik:\n{data}"

# ==============================
# TELEGRAM MESAJ HANDLER
# ==============================
async def mesaj_yakala(update: Update, context: ContextTypes.DEFAULT_TYPE):
    soru = update.message.text
    await update.message.reply_text("✍️ Düşünüyorum...")

    cevap = zai_cevap_uret(soru)

    await update.message.reply_text(cevap)

# ==============================
# BOT BAŞLAT
# ==============================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mesaj_yakala))
    print("🤖 Bot çalışıyor...")
    app.run_polling()

if __name__ == "__main__":
    main()
