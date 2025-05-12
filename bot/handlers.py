### bot/handlers.py

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
import db
from db.models import User, MediaNote, get_user_id_by_telegram_id
from .keyboards import CATEGORY_KEYBOARD, CATEGORY_MARKUP, MAIN_KEYBOARD, MAIN_MARKUP, VIEW_KEYBOARD, VIEW_MARKUP
import bot.add_note, bot.view_notes

#general handlers like start and select category

def number_to_emoji(num: int) -> str:
    emoji_map = {
        "0": "0️⃣", "1": "1️⃣", "2": "2️⃣", "3": "3️⃣", "4": "4️⃣",
        "5": "5️⃣", "6": "6️⃣", "7": "7️⃣", "8": "8️⃣", "9": "9️⃣"
    }
    return "".join(emoji_map[d] for d in str(num))


async def reset_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=MAIN_MARKUP
    )


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    language_code = update.effective_user.language_code
    
    User.get_or_create(tg_user_id, first_name,  language_code)

    await update.message.reply_text(
        "Привет! Я помогу сохранить любимые фильмы, книги и список покупок.\nВыберите действие:",
        reply_markup=MAIN_MARKUP
    )


async def handle_category_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    category_map = {
        "🎬 Cinema": "Cinema",
        "📚 Book": "Book",
        "🛒 Shop": "Shop",
        "📌 Note": "Note",
        "🧾 To Do": "To Do"
    }
    category = category_map.get(text)
    if not category:
        await update.message.reply_text("Пожалуйста, выберите категорию с помощью кнопок.")
        return

    #breakpoint()
    mode = context.user_data.get("mode")

    if mode == "add":
        context.user_data["category"] = category
        context.user_data["awaiting_title"] = True
        await update.message.reply_text("Введите название:")

    elif mode == "view":
        tg_user_id = update.effective_user.id
        await bot.view_notes.show_notes_by_category(update, context, tg_user_id, category)

    else:
        await update.message.reply_text("Пожалуйста, сначала выберите действие: New или View.")





    


        