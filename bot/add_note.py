### bot/add_note.py

from telegram import Update
from telegram.ext import ContextTypes
from db.models import MediaNote, get_user_id_by_telegram_id
from .view_notes import show_notes_by_category
from .keyboards import CATEGORY_KEYBOARD, CATEGORY_MARKUP, MAIN_KEYBOARD, MAIN_MARKUP, VIEW_KEYBOARD, VIEW_MARKUP


#ввод названия и сохранение заметки
async def handle_title_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_title"):
        title = update.message.text
        category = context.user_data.get("category")
        tg_user_id = update.effective_user.id

        # Получаем user_id из БД
        user_id = get_user_id_by_telegram_id(tg_user_id)

        # Создаём и сохраняем заметку
        note = MediaNote(
            name=title,
            author="",  # Пока без автора
            category=category,
            status="planned",  # Пока статус по умолчанию
            user_id=user_id
        )
        note.save()

        await update.message.reply_text(
            f"✅ Заметка '{title}' добавлена в категорию {category}!",
            reply_markup=MAIN_MARKUP
        )
        #context.user_data.clear()
        context.user_data["awaiting_title"] = False
        context.user_data["mode"] = "view"
        await show_notes_by_category(update, context, tg_user_id, category)
    else:
        await update.message.reply_text("Пожалуйста, используйте кнопки для выбора действия.")