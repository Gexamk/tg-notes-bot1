### main.py

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from bot.handlers import handle_start, handle_add_note, handle_text
from config import BOT_TOKEN

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(CommandHandler("add", handle_add_note))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()


if __name__ == "__main__":
    main()
