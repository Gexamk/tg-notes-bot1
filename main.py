### main.py

#
#from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
#from bot.handlers import handle_start, reset_context
#from bot.router import handle_menu_and_typing
#from config import BOT_TOKEN
#from telegram.error import TelegramError
#import logging
#import os
#from dotenv import load_dotenv
#import logging

#def main():
#    logging.warning(f"Using bot token: {BOT_TOKEN}")
#    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

#    app.add_handler(CommandHandler("start", handle_start))
#    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_and_typing))

#    async def error_handler(update, context):
#        logging.error(f"Ошибка: {context.error}", exc_info=True)
#        if update and update.message:
#            await update.message.reply_text("❌ Произошла ошибка. Начнём сначала.")
#            await reset_context(update, context)

#    app.add_error_handler(error_handler)

#    app.run_polling()


#if __name__ == "__main__":
#    main()

import logging
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config import BOT_TOKEN, WEBHOOK_SECRET_TOKEN

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)

# Telegram bot
telegram_app = Application.builder().token(BOT_TOKEN).build()

# Простейшие хендлеры
async def start(update: Update, context):
    await update.message.reply_text("Привет! Бот работает.")

async def echo(update: Update, context):
    await update.message.reply_text(f"Ты написал: {update.message.text}")

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Webhook endpoint
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != WEBHOOK_SECRET_TOKEN:
        logger.warning("❌ Неверный секретный токен")
        return "Unauthorized", 401

    try:
        update = Update.de_json(request.get_json(force=True), telegram_app.bot)
        logger.info("✅ Update получен и добавлен в очередь: %s", update)
        telegram_app.update_queue.put_nowait(update)
    except Exception as e:
        logger.exception("❌ Ошибка обработки update: %s", e)

    return "OK", 200

# Запуск Flask и Telegram
if __name__ == "__main__":
    logger.info("🚀 Старт приложения...")

    # Запуск Telegram-приложения в фоне
    async def run_telegram():
        await telegram_app.initialize()
        logger.info("✅ Telegram приложение инициализировано")
        await telegram_app.start()
        logger.info("📬 Telegram приложение запущено")

    asyncio.get_event_loop().create_task(run_telegram())

    # Запуск Flask
    app.run(host="0.0.0.0", port=8080)