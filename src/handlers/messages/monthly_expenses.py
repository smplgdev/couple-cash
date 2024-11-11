import calendar
from datetime import date

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import UserRelationship
from src.db.commands import get_user_expenses_by_month, get_active_expense_months
from src.filters.linked_users import LinkedUsersFilter
from src.keyboards import MONTHLY_EXPENSES
from src.utils.calendar import MonthNavigatorKeyboard, NavigatorCallback
from src.utils.expenses_as_text import get_expenses_as_text
from src.utils.send_probably_long_message import send_probably_long_message

router = Router()


@router.message(LinkedUsersFilter(), F.text == MONTHLY_EXPENSES)
async def show_calendar_handler(message: Message, session: AsyncSession, relationship: UserRelationship):
    active_months = await get_active_expense_months(session, relationship)
    calendar_kb = MonthNavigatorKeyboard(active_months)
    await message.answer(
        "Please, select the month you want to see the expenses for:",
        reply_markup=calendar_kb.as_markup()
    )


@router.callback_query(LinkedUsersFilter(), NavigatorCallback.filter())
async def process_months_keyboard(call: CallbackQuery, callback_data: NavigatorCallback, bot: Bot,
                                  session: AsyncSession, relationship: UserRelationship):
    year = callback_data.year
    month = callback_data.month
    if not month:
        active_months = await get_active_expense_months(session, relationship)
        calendar_kb = MonthNavigatorKeyboard(active_months, year)
        await call.message.edit_reply_markup(reply_markup=calendar_kb.as_markup())
        return

    month_str = calendar.month_name[month]

    expenses = await get_user_expenses_by_month(session, date(year, month, 1), relationship)
    if len(expenses) == 0:
        await call.answer(f"You don't have any expenses in {month_str}, {year}!", show_alert=True)
        return

    expenses_text = get_expenses_as_text(expenses, call.from_user.id)

    expenses_text = '\n'.join([
        f"Your expenses in {month_str} ({year}):",
        expenses_text,
    ])

    await send_probably_long_message(bot, call.from_user.id, expenses_text)
