from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import main_menu_keyboard, link_user_markup
from db.commands import create_or_update_user
from filters.linked_users import LinkedUsersFilter

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, session: AsyncSession, state: FSMContext):
    await state.clear()

    await create_or_update_user(
        session=session,
        tg_id=message.from_user.id,
        tg_username=message.from_user.username,
        tg_first_name=message.from_user.first_name,
        tg_language_code=message.from_user.language_code,
        return_user=False
    )
    await message.answer(
        f"Hello, {message.from_user.full_name}!\n\nTo start using me, press button below!",
        reply_markup=main_menu_keyboard
    )


@router.message(~LinkedUsersFilter())
async def not_linked_user_handler(message: Message):
    await message.answer(
        "You are not linked with any partner. Please, link with your partner to start using me!",
        reply_markup=link_user_markup
    )
