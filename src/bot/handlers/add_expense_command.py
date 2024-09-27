from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from db.commands import add_expense

router = Router()


@router.message(Command("add_expense"))
async def expense_command_handler(message: Message, command: CommandObject, session: AsyncSession):
    amount = float(command.args)
    await add_expense(session, message.from_user.id, amount)
    await message.answer(f"Expense {amount} added!")
