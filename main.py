import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ZAI_API_KEY = os.environ.get("ZAI_API_KEY")

if not BOT_TOKEN or not ZAI_API_KEY:
    raise RuntimeError("BOT_TOKEN veya ZAI_API_KEY eksik")

ZAI_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

async def mesaj_yakala(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message.text:
            await update.message.reply_text("Şimdilik sadece metin gönder.")
            return

        kullanici_sorusu = update.message.text

        prompt = f"""
Aşağıdaki matematik sorusuna BENZER,
6–8. sınıf seviyesinde,
beceri temelli,
2 adet yeni soru üret.

Her soru için:
- 4 şık (A,B,C,D)
- Tek doğru cevap
- Şıkları açık ve net yaz

Soru:
{kullanici_sorusu}
"""

        payload = {
            "model": "glm-4",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        headers = {
            "Authorization": f"Bearer {ZAI_API_KEY}",
            "Content-Type": "application/json"
        }

        r = requests.post(ZAI_URL, json=payload, headers=headers, timeout=60)
        r.raise_for_status()

        cevap = r.json()["choices"][0]["message"]["content"]

        await update.message.reply_text(cevap)

    except Exception as e:
        await update.message.reply_text("❌ Hata:\n" + str(e))

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, mesaj_yakala))
app.run_polling()
