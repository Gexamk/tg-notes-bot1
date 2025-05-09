import logging
import asyncio
import threading
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ContextTypes, filters
)
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
telegram_app.add_handler(CommandHandler("start", handle_start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_and_typing))

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('X-Telegram-Bot-Api-Secret-Token') != WEBHOOK_SECRET_TOKEN:
        return 'Unauthorized', 401

    try:
        update = Update.de_json(request.get_json(force=True), telegram_app.bot)
        telegram_app.update_queue.put_nowait(update)
        logging.info("✅ Update received and added to queue")
    except Exception as e:
        logging.exception("Ошибка при обработке запроса")

    return 'OK'

# Запуск Telegram-бота в фоновом потоке
def start_telegram_in_thread():
    async def runner():
        await telegram_app.initialize()
        await telegram_app.start()
        await telegram_app.updater.start_polling()
        logging.info("🚀 Telegram dispatcher is running")

    asyncio.run(runner())

if __name__ == '__main__':
    threading.Thread(target=start_telegram_in_thread, daemon=True).start()
    logging.info("🌐 Flask app starting on port 8080")
    app.run(host='0.0.0.0', port=8080)