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

import time
import logging
from flask import Flask

# Настройка логирования
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, this is a test endpoint!"

# Функция для записи лога каждую секунду
def log_every_30_seconds():
    while True:
        logging.info("Application is running and logging every 30 seconds.")
        time.sleep(30)  # Пауза в 30 секунд

if __name__ == '__main__':
    # Запускаем логирование в отдельном потоке
    from threading import Thread
    log_thread = Thread(target=log_every_30_seconds, daemon=True)
    log_thread.start()

    # Запускаем Flask приложение
    app.run(host='0.0.0.0', port=8080)