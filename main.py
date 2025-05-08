### main.py

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from bot.handlers import handle_start, reset_context
from bot.router import handle_menu_and_typing
from config import BOT_TOKEN
from telegram.error import TelegramError
import logging
import os
from dotenv import load_dotenv
import logging

def main():
    logging.warning(f"Using bot token: {BOT_TOKEN}")
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_and_typing))

    async def error_handler(update, context):
        logging.error(f"Ошибка: {context.error}", exc_info=True)
        if update and update.message:
            await update.message.reply_text("❌ Произошла ошибка. Начнём сначала.")
            await reset_context(update, context)

    app.add_error_handler(error_handler)

    app.run_polling()


if __name__ == "__main__":
    main()
