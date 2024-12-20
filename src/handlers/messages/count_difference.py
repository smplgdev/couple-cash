from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import UserRelationship
from src.db.commands import get_all_expenses
from src.filters.linked_users import LinkedUsersFilter

router = Router()

PAY_FOR_MY_PARTNER = "Payed for my partner"
PAY_FOR_MYSELF = "Payed for myself"
SPLIT_THE_EXPENSE = "Split the bill"


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
