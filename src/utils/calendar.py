import calendar
from datetime import datetime

from aiogram.filters.callback_data import CallbackData
from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.db import UserRelationship
from src.db.commands import get_active_expense_months


class NavigatorCallback(CallbackData, prefix="navigator"):
    year: int
    month: int | None = None


class IngoreCallback(CallbackData, prefix="navigator_ignore"):
    pass


class MonthNavigatorKeyboard:
    ignore_callback = IngoreCallback().pack()
    ignore_button = InlineKeyboardButton(text="-", callback_data=ignore_callback)

    def __init__(self, active_months: list[tuple] = None, year: int = datetime.now().year):
        self.active_months = active_months
        self.year = year

    def _navigate_year_buttons(self) -> list[InlineKeyboardButton]:
        buttons = list()
        prev_year = self.year - 1
        next_year = self.year + 1
        buttons.append(
            InlineKeyboardButton(
                text="<< " + str(prev_year),
                callback_data=NavigatorCallback(year=prev_year).pack()
            )
        )
        buttons.append(
            InlineKeyboardButton(text=str(self.year), callback_data=self.ignore_callback)
        )
        buttons.append(
            InlineKeyboardButton(
                text=str(next_year) + " >>",
                callback_data=NavigatorCallback(year=next_year).pack()
            )
        )
        return buttons

    def _get_active_months_buttons(self) -> list[InlineKeyboardButton]:
        buttons = list()
        for year, month in self.active_months:
            if year != self.year:
                continue
            buttons.append(InlineKeyboardButton(
                text=str(calendar.month_name[month]),
                callback_data=NavigatorCallback(year=year, month=month).pack()
            ))
        return buttons

    def as_markup(self):
        builder = InlineKeyboardBuilder()

        buttons = list()
        if self.active_months:
            buttons.extend(self._get_active_months_buttons())
        else:
            for i in range(1, 13):
                buttons.append(
                    InlineKeyboardButton(
                        text=calendar.month_name[i],
                        callback_data=NavigatorCallback(
                            year=self.year,
                            month=i
                        ).pack()
                    )
                )
        builder.add(*buttons)
        builder.adjust(1)
        builder.row(*self._navigate_year_buttons())
        return builder.as_markup()
