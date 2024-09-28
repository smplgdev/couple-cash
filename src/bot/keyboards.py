from typing import Iterable

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

LINK_YOUR_PARTNER = "Link your partner"
ADD_EXPENSE = "Add expense"
COUNT_DIFFERENCE = "Count difference"

PAY_FOR_MYSELF = "Pay for myself"
PAY_FOR_MY_PARTNER = "Pay for my partner"
SPLIT_THE_EXPENSE = "Split the expense"

main_menu_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=ADD_EXPENSE),
    ],
    [
        KeyboardButton(text=COUNT_DIFFERENCE),
    ]
], resize_keyboard=True)

link_user_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=LINK_YOUR_PARTNER),
    ],
], resize_keyboard=True)

payment_type_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text=PAY_FOR_MYSELF),
        KeyboardButton(text=PAY_FOR_MY_PARTNER),
    ],
    [
        KeyboardButton(text=SPLIT_THE_EXPENSE),
    ]
], resize_keyboard=True)


def categories_markup(categories: Iterable) -> ReplyKeyboardMarkup:
    keyboard = []
    for category in set(categories):
        keyboard.append([KeyboardButton(text=category)])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
