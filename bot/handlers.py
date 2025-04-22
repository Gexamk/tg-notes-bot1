### bot/handlers.py

from telegram import Update
from telegram.ext import ContextTypes
from db.models import User, MediaNote


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_user_id = update.effective_user.id
    User.get_or_create(tg_user_id)
    await update.message.reply_text("Привет! Я помогу тебе сохранять любимые книги, фильмы и музыку.")


async def handle_add_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пока это просто заглушка. Здесь будет логика добавления заметки.")