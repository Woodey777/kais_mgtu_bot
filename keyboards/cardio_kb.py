from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

def cardio_type_kb() -> InlineKeyboardMarkup:
    kb_list = [
        [InlineKeyboardButton(text="Бег",                 callback_data="running_type"), 
         InlineKeyboardButton(text="Плавание",            callback_data="swimming_type")], 
        [InlineKeyboardButton(text="Ролики",              callback_data="rollers_type"), 
         InlineKeyboardButton(text="Коньки",              callback_data="ice_skates_type")], 
        [InlineKeyboardButton(text="Лыжи",                callback_data="ski_type"), 
         InlineKeyboardButton(text="Велосипед",           callback_data="cycle_type")], 
        [InlineKeyboardButton(text="Беговой факультатив", callback_data="running_fac_type"), 
         InlineKeyboardButton(text="Рогейн 20+км",        callback_data="rogaine_type")], 
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def trainings_kb() -> InlineKeyboardMarkup:
    kb_list = [
        [InlineKeyboardButton(text="Кардио",  callback_data="add_cardio")],
        [InlineKeyboardButton(text="Лазание", callback_data="add_climbing")]
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


def pay_debt_kb() -> InlineKeyboardMarkup:
    kb_list = [
        [InlineKeyboardButton(text="Да",  callback_data="yes_pay_debt")],
        [InlineKeyboardButton(text="Нет", callback_data="no_pay_debt")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def send_cardio_kb() -> InlineKeyboardMarkup:
    kb_list = [
        [InlineKeyboardButton(text="Отправить",         callback_data="send_cardio")],
        [InlineKeyboardButton(text="Заполнить еще раз", callback_data="cardio_again")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard