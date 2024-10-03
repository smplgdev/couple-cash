from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from notion.api import get_db_props

ADD_EXPENSE = "Add expense"
COUNT_DIFFERENCE = "Count difference"
RECENT_EXPENSES = "Recent expenses"

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
            KeyboardButton(text=RECENT_EXPENSES),
        ],
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
