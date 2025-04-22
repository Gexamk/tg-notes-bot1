### bot/handlers.py

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from db.models import User, MediaNote

CATEGORY_KEYBOARD = [["🎬 Cinema", "📚 Book", "🎵 Song"]]
CATEGORY_MARKUP = ReplyKeyboardMarkup(CATEGORY_KEYBOARD, resize_keyboard=True)


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_user_id = update.effective_user.id
    User.get_or_create(tg_user_id)

    keyboard = [["➕ New", "📋 View"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Привет! Я помогу сохранить любимые фильмы, книги и песни.\nВыберите действие:",
        reply_markup=reply_markup
    )


async def handle_add_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Выберите категорию для новой заметки:",
        reply_markup=CATEGORY_MARKUP
    )


async def handle_category_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    category_map = {
        "🎬 Cinema": "Cinema",
        "📚 Book": "Book",
        "🎵 Song": "Song"
    }
    category = category_map.get(text)
    if not category:
        await update.message.reply_text("Пожалуйста, выберите категорию с помощью кнопок.")
        return

    mode = context.user_data.get("mode")
    if mode == "add":
        context.user_data["category"] = category
        context.user_data["awaiting_title"] = True
        await update.message.reply_text("Введите название (например: В бой идут одни старики):")
    elif mode == "view":
        await update.message.reply_text(f"Вы выбрали {text} для просмотра заметок.")
        # TODO: implement viewing logic
    else:
        await update.message.reply_text("Пожалуйста, сначала выберите действие: New или View.")


async def handle_title_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_title"):
        title = update.message.text
        context.user_data["title"] = title
        context.user_data["awaiting_title"] = False

        await update.message.reply_text(f"Название '{title}' сохранено. Скоро добавим в базу 😉")
    else:
        await update.message.reply_text("Пожалуйста, используйте кнопки для выбора действия.")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    elif context.user_data.get("awaiting_title"):
        await handle_title_input(update, context)
    else:
        await update.message.reply_text("Пожалуйста, используйте кнопки для выбора действия.")