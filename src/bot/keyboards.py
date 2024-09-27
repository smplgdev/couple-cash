from typing import Iterable

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Add expense"),
    ]
], resize_keyboard=True)


payment_type_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Pay for myself"),
        KeyboardButton(text="Pay for my partner"),
    ],
    [
        KeyboardButton(text="Split the expense"),
    ]
], resize_keyboard=True)


def markup_of_categories(categories: Iterable) -> ReplyKeyboardMarkup:
    keyboard = []
    for category in set(categories):
        keyboard.append([KeyboardButton(text=category)])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
