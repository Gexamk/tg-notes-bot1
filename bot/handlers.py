### bot/handlers.py

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from db.models import User, MediaNote
import db

CATEGORY_KEYBOARD = [["🎬 Cinema", "📚 Book", "🎵 Song"]]
CATEGORY_MARKUP = ReplyKeyboardMarkup(CATEGORY_KEYBOARD, resize_keyboard=True)

MAIN_KEYBOARD = [["➕ New", "📋 View"]]
MAIN_MARKUP = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)


async def reset_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=MAIN_MARKUP
    )


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_user_id = update.effective_user.id
    User.get_or_create(tg_user_id)

    DEFAULT_KEYBOARD = [["➕ New", "📋 View"]]
    DEFAULT_MARKUP = ReplyKeyboardMarkup(DEFAULT_KEYBOARD, resize_keyboard=True)

    await update.message.reply_text(
        "Привет! Я помогу сохранить любимые фильмы, книги и песни.\nВыберите действие:",
        reply_markup=MAIN_MARKUP
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
        await update.message.reply_text("Введите название (например: Бесы):")
    elif mode == "view":
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE telegram_id = %s", (tg_user_id,))
            user_row = cur.fetchone()
            if not user_row:
                await update.message.reply_text("Пользователь не найден. Пожалуйста, начните заново.")
                return
            user_id = user_row["id"]

            cur.execute("""
                SELECT name, created_at FROM media_notes
                WHERE user_id = %s AND category = %s
                ORDER BY created_at DESC
            """, (user_id, category))
            notes = cur.fetchall()

        if not notes:
            await update.message.reply_text(f"Нет заметок в категории {text}.")
        else:
            note_lines = [f"• {row['name']} ({row['created_at'].strftime('%Y-%m-%d')})" for row in notes]
            await update.message.reply_text(
                f"Ваши заметки в категории {text}:\n" + "\n".join(note_lines)
            )

        await reset_context(update, context)
    else:
        await update.message.reply_text("Пожалуйста, сначала выберите действие: New или View.")


async def handle_title_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_title"):
        title = update.message.text
        category = context.user_data.get("category")
        tg_user_id = update.effective_user.id

        # Получаем user_id из БД
        conn = db.get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE telegram_id = %s", (tg_user_id,))
            user_row = cur.fetchone()
            if not user_row:
                await update.message.reply_text("Пользователь не найден. Пожалуйста, начните заново.")
                return
            user_id = user_row["id"]

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
        await reset_context(update, context)
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