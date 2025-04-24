### bot/status_and_delete.py


from telegram import Update
from telegram.ext import ContextTypes
from db.models import MediaNote
from .view_notes import show_notes_by_category
from .keyboards import CATEGORY_KEYBOARD, CATEGORY_MARKUP, MAIN_KEYBOARD, MAIN_MARKUP, VIEW_KEYBOARD, VIEW_MARKUP

#меняем статус или удаляем по введеному индексу           
async def handle_number_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text.isdigit():
        await update.message.reply_text("Введите номер заметки цифрой.")
        return

    index = int(text) - 1
    notes = context.user_data.get("notes")
    action = context.user_data.get("action")

    if notes is None or action is None:
        await update.message.reply_text("Нет активного списка или действия.")
        return

    if index < 0 or index >= len(notes):
        await update.message.reply_text("Неверный номер. Попробуйте снова.")
        return

    note_id = notes[index]["id"]
    name = notes[index]["name"]
    category = notes[index]["category"]

    if action == "toggle_status":
        current_status = notes[index]["status"]
        new_status = "done" if current_status != "done" else "planned"
        MediaNote.update_status(note_id, new_status)
        await update.message.reply_text("Статус обновлен.")

    elif action == "delete":
        MediaNote.delete(note_id)
        await update.message.reply_text(f"Заметка '{name}' удалена из категории {category}.")

    tg_user_id = update.effective_user.id
    context.user_data["action"] = ""
    #category = context.user_data.get("category") не понятно почем в контексте пусто, пока поменяю

    await show_notes_by_category(update, context, tg_user_id, category)