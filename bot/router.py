### bot/router.py

from telegram import Update
from telegram.ext import ContextTypes
from .handlers import handle_category_selection, reset_context
from .add_note import handle_title_input
from .status_and_delete import handle_number_input
from .keyboards import CATEGORY_KEYBOARD, CATEGORY_MARKUP, MAIN_KEYBOARD, MAIN_MARKUP, VIEW_KEYBOARD, VIEW_MARKUP
import bot.keyboards


async def handle_menu_and_typing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "➕ New":
        context.user_data["mode"] = "add"
        await update.message.reply_text(
            "Выберите категорию для новой заметки:",
            reply_markup=CATEGORY_MARKUP
        )
    elif text == "📋 View":
        context.user_data["mode"] = "view"
        await update.message.reply_text(
            "Выберите категорию для просмотра заметок:",
            reply_markup=CATEGORY_MARKUP
        )
    elif text in ["🎬 Cinema", "📚 Book", "🎵 Song"]:
        await handle_category_selection(update, context)
    elif text == "✅ Mark|Unmark":
        context.user_data["action"] = "toggle_status"
        await update.message.reply_text("Введите номер заметки для изменения статуса:")
    elif text == "🗑 Delete":
        context.user_data["action"] = "delete"
        await update.message.reply_text("Введите номер заметки для удаления:")
    elif text == "🔙 Back":
        await reset_context(update, context)
    elif context.user_data.get("awaiting_title"):
        await handle_title_input(update, context)
    elif context.user_data.get("action") in ["toggle_status", "delete"]:
        await handle_number_input(update, context)        
    else:
        await update.message.reply_text("Пожалуйста, используйте кнопки для выбора действия.")