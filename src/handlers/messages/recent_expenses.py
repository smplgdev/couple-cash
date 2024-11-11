from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import UserRelationship
from src.db.commands import get_recent_expenses
from src.filters.linked_users import LinkedUsersFilter
from src.keyboards import RECENT_EXPENSES
from src.utils.expenses_as_text import get_expenses_as_text
from src.utils.send_probably_long_message import send_probably_long_message

router = Router()


@router.message(LinkedUsersFilter(), F.text == RECENT_EXPENSES)
async def last_expenses_handler(message: Message, state: FSMContext, bot: Bot,
                                session: AsyncSession, relationship: UserRelationship):
    await state.clear()
    expenses = await get_recent_expenses(session, relationship)
    expenses_text = get_expenses_as_text(expenses, message.from_user.id)
    expenses_text = '\n'.join([
        f"Your spending over the last 30 days:\n",
        expenses_text,
    ])
    await send_probably_long_message(bot, message.from_user.id, expenses_text)
