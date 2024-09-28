from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import PAY_FOR_MY_PARTNER, SPLIT_THE_EXPENSE, PAY_FOR_MYSELF
from db import UserRelationship
from db.commands import get_all_expenses
from filters.linked_users import LinkedUsersFilter

router = Router()


@router.message(LinkedUsersFilter(), F.text == "Count difference")
async def count_difference_handler(message: Message, session: AsyncSession, relationship: UserRelationship):
    expenses = await get_all_expenses(session, relationship)

    difference = 0
    for expense in expenses:
        value = 0
        if expense.user_tg_id == message.from_user.id and expense.payment_type == PAY_FOR_MY_PARTNER:
            value = -expense.amount
        elif expense.user_tg_id == message.from_user.id and expense.payment_type == SPLIT_THE_EXPENSE:
            value = -(expense.amount / 2)
        elif expense.user_tg_id != message.from_user.id and expense.payment_type == SPLIT_THE_EXPENSE:
            value = expense.amount / 2
        elif expense.user_tg_id != message.from_user.id and expense.payment_type == PAY_FOR_MY_PARTNER:
            value = expense.amount
        difference += value

    if difference < 0:
        text = "Your partner owes you %s €" % str(round(abs(difference), 2)).replace(".", ",")
    else:
        text = "You owe your partner %s €" % str(round(difference, 2)).replace(".", ",")

    await message.answer(text)
