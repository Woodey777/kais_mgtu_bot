from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def climb_type_kb() -> InlineKeyboardMarkup:
    kb_list = [
        [InlineKeyboardButton(text="Трудность с нижней страховкой",  callback_data="climb_low_type")], 
        [InlineKeyboardButton(text="Трудность с верхней страховкой", callback_data="climb_high_type")], 
        [InlineKeyboardButton(text="Болдеринг",                      callback_data="bouldering_type"), 
         InlineKeyboardButton(text="Драйтулинг",                     callback_data="drytool_type")], 
        [InlineKeyboardButton(text="Ледолазание",                    callback_data="ice_climb_type")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def is_competition_kb() -> InlineKeyboardMarkup:
    kb_list = [
        [InlineKeyboardButton(text="Да",  callback_data="yes_competition")],
        [InlineKeyboardButton(text="Нет", callback_data="no_competition")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def send_climbing_kb() -> InlineKeyboardMarkup:
    kb_list = [
        [InlineKeyboardButton(text="Отправить",         callback_data="send_climbing")],
        [InlineKeyboardButton(text="Заполнить еще раз", callback_data="climbing_again")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard