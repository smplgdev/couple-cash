from typing import Iterable

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from notion.api import get_db_props

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


def get_property_keyboard(prop: str) -> ReplyKeyboardMarkup:
    options = get_db_props()[prop]['options']

    builder = ReplyKeyboardBuilder()
    for option in options:
        builder.button(text=option)
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


payment_type_keyboard = get_property_keyboard(select_types["PAYMENT_TYPE"])
category_keyboard = get_property_keyboard(select_types["CATEGORY"])
subcategory_keyboard = get_property_keyboard(select_types["SUBCATEGORY"])
