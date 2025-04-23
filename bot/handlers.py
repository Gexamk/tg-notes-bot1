### bot/handlers.py

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from db.models import User, MediaNote, get_user_id_by_telegram_id
import db

CATEGORY_KEYBOARD = [["🎬 Cinema", "📚 Book", "🎵 Song"], ["🔙 Back"]]
CATEGORY_MARKUP = ReplyKeyboardMarkup(CATEGORY_KEYBOARD, resize_keyboard=True)

MAIN_KEYBOARD = [["➕ New", "📋 View"]]
MAIN_MARKUP = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)

VIEW_KEYBOARD = [["✅ Mark|Unmark", "🗑 Delete"], ["🔙 Back"]]
VIEW_MARKUP = ReplyKeyboardMarkup(VIEW_KEYBOARD, resize_keyboard=True)

async def reset_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=MAIN_MARKUP
    )


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_user_id = update.effective_user.id
    User.get_or_create(tg_user_id)

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
        tg_user_id = update.effective_user.id
        await show_notes_by_category(update, context, tg_user_id, category)

    else:
        await update.message.reply_text("Пожалуйста, сначала выберите действие: New или View.")


async def show_notes_by_category(update: Update, context: ContextTypes.DEFAULT_TYPE, tg_user_id: int, category: str):
    user_id = get_user_id_by_telegram_id(tg_user_id)
    if not user_id:
        await update.message.reply_text("Пользователь не найден. Пожалуйста, начните заново.")
        return

    conn = db.get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, name, category, status FROM media_notes
            WHERE user_id = %s AND category = %s
            ORDER BY created_at ASC
        """, (user_id, category))
        notes = cur.fetchall()

    if not notes:
        await update.message.reply_text("Заметки не найдены в этой категории.", reply_markup=MAIN_MARKUP)
    else:
        context.user_data["notes"] = notes
        response_lines = []
        for i, note in enumerate(notes):
            status_emoji = "✅" if note["status"] == "done" else ""
            response_lines.append(f"{i + 1}️⃣ {note['name']} {status_emoji}")
        response = "\n".join(response_lines)
        await update.message.reply_text(f"📂 {category}:", reply_markup=VIEW_MARKUP)
        await update.message.reply_text(response)

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

    if action == "toggle_status":
        current_status = notes[index]["status"]
        new_status = "done" if current_status != "done" else "planned"
        MediaNote.update_status(note_id, new_status)
        await update.message.reply_text("Статус обновлен.")

    elif action == "delete":
        MediaNote.delete(note_id)
        await update.message.reply_text("Заметка удалена.")

    tg_user_id = update.effective_user.id
    #category = context.user_data.get("category") не понятно почем в контексте пусто, пока поменяю
    category = notes[index]["category"] 

    await show_notes_by_category(update, context, tg_user_id, category)
