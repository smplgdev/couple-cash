from typing import Iterable

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Add expense"),
    ],
    [
        KeyboardButton(text="Count difference"),
    ]
], resize_keyboard=True)


PAY_FOR_MYSELF = "Pay for myself"
PAY_FOR_MY_PARTNER = "Pay for my partner"
SPLIT_THE_EXPENSE = "Split the expense"


payment_type_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=PAY_FOR_MYSELF),
        KeyboardButton(text=PAY_FOR_MY_PARTNER),
    ],
    [
        KeyboardButton(text=SPLIT_THE_EXPENSE),
    ]
], resize_keyboard=True)


def markup_of_categories(categories: Iterable) -> ReplyKeyboardMarkup:
    keyboard = []
    for category in set(categories):
        keyboard.append([KeyboardButton(text=category)])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
