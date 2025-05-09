import logging
import asyncio
from threading import Thread
from queue import Queue
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters

from config import BOT_TOKEN, WEBHOOK_SECRET_TOKEN
from bot.handlers import handle_start
from bot.router import handle_menu_and_typing

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

update_queue = Queue()

telegram_app = Application.builder().token(BOT_TOKEN).build()
telegram_app.add_handler(CommandHandler("start", handle_start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_and_typing))

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('X-Telegram-Bot-Api-Secret-Token') != WEBHOOK_SECRET_TOKEN:
        return 'Unauthorized', 401
    try:
        update = Update.de_json(request.get_json(force=True), telegram_app.bot)
        logging.info("✅ Update received and added to queue")
        update_queue.put(update)
    except Exception:
        logging.exception("❌ Ошибка при обработке запроса")
    return 'OK'

async def telegram_worker():
    await telegram_app.initialize()
    await telegram_app.start()
    logging.info("🚀 Telegram dispatcher is running")

    while True:
        update = await asyncio.to_thread(update_queue.get)
        try:
            await telegram_app.process_update(update)
        except Exception as e:
            logging.exception("Ошибка в обработчике: %s", e)

def start_telegram():
    asyncio.run(telegram_worker())

if __name__ == '__main__':
    thread = Thread(target=start_telegram)
    thread.start()
    logging.info("🌐 Flask app starting")
    app.run(host='0.0.0.0', port=8080)