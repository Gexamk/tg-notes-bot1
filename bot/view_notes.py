### bot/view_notes.py

from telegram import Update
from telegram.ext import ContextTypes
from .keyboards import CATEGORY_KEYBOARD, CATEGORY_MARKUP, MAIN_KEYBOARD, MAIN_MARKUP, VIEW_KEYBOARD, VIEW_MARKUP
from db.models import get_user_id_by_telegram_id
import bot.handlers 
import db, db.models
import logging

async def show_notes_by_category(update: Update, context: ContextTypes.DEFAULT_TYPE, tg_user_id: int, category: str):
    user_id = get_user_id_by_telegram_id(tg_user_id)
    if not user_id:
        await update.message.reply_text("Пользователь не найден. Пожалуйста, начните заново.")
        return

    conn = db.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, name, category, status FROM media_notes
                WHERE user_id = %s AND category = %s
                ORDER BY created_at ASC
            """, (user_id, category))
            notes = cur.fetchall()
    finally:
        logging.info("❌ exception in getting list of notes by category within DB interaction")
        release_connection(conn) 

    if not notes:
        await update.message.reply_text("Заметки не найдены в этой категории.", reply_markup=MAIN_MARKUP)
    else:
        context.user_data["notes"] = notes
        response_lines = []
        for i, note in enumerate(notes):
            status_emoji = "✅" if note["status"] == "done" else ""
            number_emoji = bot.handlers.number_to_emoji(i + 1)
            response_lines.append(f"{number_emoji} {note['name']} {status_emoji}")
        response = "\n".join(response_lines)
        await update.message.reply_text(f"📂 {category}:", reply_markup=VIEW_MARKUP)
        await update.message.reply_text(response)