from datetime import timedelta, date

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.operators import and_

from src.db import UserRelationship, Expense
from src.filters.linked_users import LinkedUsersFilter
from src.handlers.messages.count_difference import PAY_FOR_MY_PARTNER, SPLIT_THE_EXPENSE, PAY_FOR_MYSELF
from src.keyboards import RECENT_EXPENSES
from src.utils.send_probably_long_message import send_probably_long_message

router = Router()


async def get_recent_expenses_text(session: AsyncSession, relationship: UserRelationship, user_tg_id: int, period: int = 30):
    stmt = (
        select(Expense).
        where(
            and_(
                Expense.user_tg_id.in_([relationship.initiating_user_tg_id, relationship.partner_user_tg_id]),
                Expense.created_at >= date.today() - timedelta(days=period)
            )
        ).
        order_by(Expense.created_at.desc()).
        options(selectinload(Expense.user))
    )
    result = await session.execute(stmt)
    expenses = result.scalars().all()

    text_parts = list()
    text_parts.append(f"Your spending over the last {30} days:\n")
    spent: float = 0

    for expense in expenses:
        expense_spent = 0

        if any([
            expense.payment_type == PAY_FOR_MYSELF and expense.user_tg_id == user_tg_id,
            expense.payment_type == PAY_FOR_MY_PARTNER and expense.user_tg_id != user_tg_id
        ]):
            expense_spent = expense.amount
        elif expense.payment_type == SPLIT_THE_EXPENSE:
            expense_spent = expense.amount / 2

        spent += expense_spent
        sum_text = str(round(expense_spent, 2)).replace(".", ",") + " €"
        if expense_spent != 0:
            text_parts.append(f"\n{expense.user.tg_first_name} [{expense.created_at.strftime("%d.%m at %H:%M")}]\n{sum_text}\n{expense.category}\n{expense.comment}")

    text_parts.append(hbold(f"\nYou spent in the last {period} days in total: {str(round(spent, 2)).replace(".", ",")} €"))
    return "\n".join(text_parts)


@router.message(LinkedUsersFilter(), F.text == RECENT_EXPENSES)
async def last_expenses_handler(message: Message, state: FSMContext, bot: Bot,
                                session: AsyncSession, relationship: UserRelationship):
    await state.clear()
    text = await get_recent_expenses_text(session, relationship, message.from_user.id)
    await send_probably_long_message(bot, message.from_user.id, text)
