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
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, ApplicationBuilder
from config import BOT_TOKEN, WEBHOOK_SECRET_TOKEN
from bot.router import handle_text
from bot.common import handle_start

app = Flask(__name__)

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Telegram приложение (Application в sync-режиме)
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()
telegram_app.add_handler(handle_start)
telegram_app.add_handler(handle_text)

@app.route('/')
def index():
    return "Bot is alive!"

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('X-Telegram-Bot-Api-Secret-Token') != WEBHOOK_SECRET_TOKEN:
        return 'Unauthorized', 401

    update = Update.de_json(request.get_json(force=True), telegram_app.bot)

    try:
        telegram_app.process_update(update)
        logging.info("✅ Update received and processed")
    except Exception as e:
        logging.exception("Ошибка при обработке update")

    return 'OK'

if __name__ == '__main__':
    logging.info("🚀 Starting Flask app...")
    app.run(host="0.0.0.0", port=8080)