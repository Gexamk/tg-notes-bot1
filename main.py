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

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Функция для записи лога каждые 10 секунд
def log_every_10_seconds():
    while True:
        logging.info("Application is running and logging every 10 seconds.")
        time.sleep(10)  # Пауза в 10 секунд

if __name__ == '__main__':
    # Запуск функции записи логов в фоновом потоке
    from threading import Thread
    log_thread = Thread(target=log_every_10_seconds, daemon=True)
    log_thread.start()

    # Приложение продолжает работать в фоновом режиме
    while True:
        time.sleep(1000)  # Просто цикл, чтобы приложение не завершилось