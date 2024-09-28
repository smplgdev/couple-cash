from typing import Iterable

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from notion.api import get_buttons

LINK_YOUR_PARTNER = "Link your partner"
ADD_EXPENSE = "Add expense"
COUNT_DIFFERENCE = "Count difference"

select_types = {
    "PAYMENT_TYPE": "Type of expenses",
    "CATEGORY": "Category",
    "SUBCATEGORY": "Subcategory"
}

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

payment_type_keyboard = ReplyKeyboardMarkup(
    keyboard=get_buttons(select_types["PAYMENT_TYPE"]), 
    resize_keyboard=True
)

category_keyboard = ReplyKeyboardMarkup(
    keyboard=get_buttons(select_types["CATEGORY"]), 
    resize_keyboard=True
)

subcategory_keyboard = ReplyKeyboardMarkup(
    keyboard=get_buttons(select_types["SUBCATEGORY"]), 
    resize_keyboard=True
)

def categories_markup(categories: Iterable) -> ReplyKeyboardMarkup:
    keyboard = []
    for category in set(categories):
        keyboard.append([KeyboardButton(text=category)])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
