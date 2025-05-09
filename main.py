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

import asyncio
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN, WEBHOOK_SECRET_TOKEN
from bot.handlers import handle_start, reset_context
from bot.router import handle_menu_and_typing

app = Flask(__name__)

telegram_app = Application.builder().token(BOT_TOKEN).build()
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_and_typing))
telegram_app.add_handler(CommandHandler("start", handle_start))

@app.before_first_request
def start_telegram_bot():
    logging.info("🔄 Инициализация Telegram Application...")
    loop = asyncio.get_event_loop()
    loop.create_task(telegram_app.initialize())
    loop.create_task(telegram_app.start())

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('X-Telegram-Bot-Api-Secret-Token') != WEBHOOK_SECRET_TOKEN:
        return 'Unauthorized', 401

    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)

    logging.info("📩 Update получен и добавлен в очередь")
    return 'OK'

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("🚀 Старт приложения...")
    app.run(host='0.0.0.0', port=8080)