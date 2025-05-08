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

from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN, WEBHOOK_SECRET_TOKEN
import logging
import asyncio

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG  # Уровень логирования DEBUG покажет всё
)

app = Flask(__name__)

telegram_app = Application.builder().token(BOT_TOKEN).build()

# Простейший обработчик
async def echo(update: Update, context):
    print("Получено сообщение:", update.message.text)

telegram_app.add_handler(MessageHandler(filters.TEXT, echo))

async def echo(update: Update, context):
    logging.debug(f"📩 Сообщение от пользователя: {update.message.text}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Принято")


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('X-Telegram-Bot-Api-Secret-Token') != WEBHOOK_SECRET_TOKEN:
        return 'Unauthorized', 401

    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    
    # Логируем входящие данные
    app.logger.info(f"Received update: {update.to_dict()}")

    telegram_app.update_queue.put_nowait(update)
    
    return 'OK'

# 🧠 Критический момент: инициализация Telegram App
async def run_app():
    await telegram_app.initialize()
    await telegram_app.start()
    logging.info("🚀 Telegram Application initialized and started")

if __name__ == '__main__':
    asyncio.run(run_app())  # Запускаем телеграм-бота
    app.run(port=8080)      # Запускаем Flask