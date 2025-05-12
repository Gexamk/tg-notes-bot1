### bot/keyboards.py

from telegram import ReplyKeyboardMarkup

MAIN_KEYBOARD = [["➕ New", "📋 View"]]
MAIN_MARKUP = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True, one_time_keyboard=False)

CATEGORY_KEYBOARD = [["🎬 Cinema", "📚 Book","🛒 Shop"], ["📌 Note","📝 To Do"], ["🔙 Back"]]
CATEGORY_MARKUP = ReplyKeyboardMarkup(CATEGORY_KEYBOARD, resize_keyboard=True, one_time_keyboard=False)

VIEW_KEYBOARD = [["➕ New","✅ Mark|Unmark", "🗑 Delete"], ["🔙 Back"]]
VIEW_MARKUP = ReplyKeyboardMarkup(VIEW_KEYBOARD, resize_keyboard=True, one_time_keyboard=False)