from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def mesaj_yakala(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.text:
        await update.message.reply_text(
            "📝 Metin alındı.\n\nBir sonraki aşamada bu sorudan yeni sorular üreteceğim."
        )

    elif update.message.photo:
        await update.message.reply_text(
            "🖼️ Görsel alındı.\n\nBir sonraki aşamada resimden soruyu okuyacağım."
        )

    elif update.message.document:
        await update.message.reply_text(
            "📄 Dosya alındı.\n\nBir sonraki aşamada içeriği analiz edeceğim."
        )

    else:
        await update.message.reply_text(
            "⚠️ Desteklenmeyen içerik."
        )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, mesaj_yakala))
app.run_polling()
