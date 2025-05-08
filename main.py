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
from telegram.ext import Application, ContextTypes, MessageHandler, filters
from config import BOT_TOKEN, WEBHOOK_SECRET_TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask-приложение
app = Flask(__name__)

# Telegram Application
telegram_app = Application.builder().token(BOT_TOKEN).build()

# Простой обработчик текста
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"Got message: {update.message.text}")
    await update.message.reply_text("✅ Принял!")

telegram_app.add_handler(MessageHandler(filters.TEXT, echo))

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('X-Telegram-Bot-Api-Secret-Token') != WEBHOOK_SECRET_TOKEN:
        return 'Unauthorized', 401

    try:
        update = Update.de_json(request.get_json(force=True), telegram_app.bot)
        asyncio.create_task(telegram_app.process_update(update))
        logging.info("✅ Update received and processed")
    except Exception as e:
        logging.exception("Ошибка при обработке запроса")

    return 'OK'

# Запуск Telegram App в фоне
async def start_telegram():
    await telegram_app.initialize()
    await telegram_app.start()
    logging.info("🚀 Telegram bot started")

# Запуск Flask и Telegram
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(start_telegram())
    logging.info("🌐 Flask app starting on port 8080")
    app.run(host='0.0.0.0', port=8080)