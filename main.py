### main.py

from telegram.ext import ApplicationBuilder, CommandHandler
from handlers import handle_start, handle_add_note
from config import BOT_TOKEN


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(CommandHandler("add", handle_add_note))

    app.run_polling()


if __name__ == "__main__":
    main()