import logging
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, CommandHandler, filters
from config import BOT_TOKEN, WEBHOOK_SECRET_TOKEN
from bot.router import handle_menu_and_typing
from bot.handlers import handle_start


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask-приложение
app = Flask(__name__)

# Telegram Application
telegram_app = Application.builder().token(BOT_TOKEN).build()


# Обработчики Telegram
async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Бот работает.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"📩 Message from user: {update.message.text}")
    await update.message.reply_text("✅ Принял!")

telegram_app.add_handler(CommandHandler("start", handle_start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_and_typing))

# Webhook-обработчик
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('X-Telegram-Bot-Api-Secret-Token') != WEBHOOK_SECRET_TOKEN:
        return 'Unauthorized', 401

    try:
        update = Update.de_json(request.get_json(force=True), telegram_app.bot)
        logging.info("✅ Update received and added to queue")

        # Запускаем асинхронную задачу безопасно
        asyncio.get_event_loop().create_task(telegram_app.process_update(update))
        
    except Exception:
        logging.exception("❌ Ошибка при обработке запроса")

    return 'OK'

# Запуск Telegram Application
async def run_telegram():
    await telegram_app.initialize()
    await telegram_app.start()
    logging.info("🚀 Telegram dispatcher is running")

# Запуск Flask + Telegram
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_telegram())
    logging.info("🌐 Flask app starting on port 8080")
    app.run(host="0.0.0.0", port=8080)