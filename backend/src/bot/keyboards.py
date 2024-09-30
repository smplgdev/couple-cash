from typing import Iterable

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from notion.api import get_buttons

server_link = "https://4ae59326641dac374842ceeffb80b50c.serveo.net"

ADD_EXPENSE = "Add expense"
COUNT_DIFFERENCE = "Count difference"

select_types = {
    "PAYMENT_TYPE": "Type of expenses",
    "CATEGORY": "Category",
    "SUBCATEGORY": "Subcategory"
}

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=ADD_EXPENSE),
        ],
        [
            KeyboardButton(text=COUNT_DIFFERENCE),
        ],
        [
            KeyboardButton(text="Web App", web_app=WebAppInfo(url=server_link))
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

payment_type_keyboard = ReplyKeyboardMarkup(
    keyboard=get_buttons(select_types["PAYMENT_TYPE"]), 
    resize_keyboard=True
)

category_keyboard = ReplyKeyboardMarkup(
    keyboard=get_buttons(select_types["CATEGORY"]), 
    resize_keyboard=True,
    one_time_keyboard=True
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
