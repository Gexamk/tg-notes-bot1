### bot/keyboards.py

from telegram import ReplyKeyboardMarkup

MAIN_KEYBOARD = [["➕ New", "📋 View"]]
MAIN_MARKUP = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)

CATEGORY_KEYBOARD = [["🎬 Cinema", "📚 Book", "🎵 Song"], ["🔙 Back"]]
CATEGORY_MARKUP = ReplyKeyboardMarkup(CATEGORY_KEYBOARD, resize_keyboard=True)

VIEW_KEYBOARD = [["✅ Mark|Unmark", "🗑 Delete"], ["🔙 Back"]]
VIEW_MARKUP = ReplyKeyboardMarkup(VIEW_KEYBOARD, resize_keyboard=True)