from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def start_kb() -> ReplyKeyboardMarkup:
    kb_list = [
        [KeyboardButton(text="📖 Рейтинг")],
        [KeyboardButton(text="Добавить активность")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard