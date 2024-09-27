from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from db.commands import add_expense
from filters.linked_users import LinkedUsersFilter

router = Router()


@router.message(LinkedUsersFilter(), Command("expense"))
async def expense_command_handler(message: Message, command: CommandObject, session: AsyncSession):
    amount = float(command.args)
    is_added = await add_expense(session, message.from_user.id, amount)
    if not is_added:
        await message.answer(f"Failed to add expense {amount}")
        return
    await message.answer(f"Expense {amount} added!")


@router.message(Command("expense"))
async def not_linked_user_handler(message: Message):
    await message.answer("You are not linked with any user so far.")
