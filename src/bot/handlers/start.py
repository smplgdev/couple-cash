from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hcode
from sqlalchemy.ext.asyncio import AsyncSession

from db.commands import create_or_update_user

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, session: AsyncSession):
    await create_or_update_user(
        session=session,
        tg_id=message.from_user.id,
        tg_username=message.from_user.username,
        tg_first_name=message.from_user.first_name,
        tg_language_code=message.from_user.language_code,
        return_user=False
    )
    await message.answer(f"Hello, {message.from_user.full_name}!\n\nTo start using me, just send command {hcode("/expense <amount>")}!")
