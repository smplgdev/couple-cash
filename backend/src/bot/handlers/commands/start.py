from aiogram import Router, Bot
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import main_menu_keyboard
from db.commands import create_or_update_user, get_user_or_none, create_user_relationship

router = Router()


@router.message(CommandStart(deep_link=True))
async def start_command_with_deep_link(message: Message, session: AsyncSession, command: CommandObject, bot: Bot):
    await create_or_update_user(
        session=session,
        tg_id=message.from_user.id,
        tg_username=message.from_user.username,
        tg_first_name=message.from_user.first_name,
        tg_language_code=message.from_user.language_code,
        return_user=False
    )
    partner_user = await get_user_or_none(session, int(command.args))
    if not partner_user:
        await message.answer("Your partner has not been found...")
        return
    elif partner_user.tg_id == message.from_user.id:
        await message.answer("You can't invite yourself")
        return

    await create_user_relationship(session, message.from_user.id, partner_user.tg_id)

    await message.answer(
        f"Hello, {message.from_user.full_name}!\n\nYou were invited by {partner_user.tg_first_name}. To start using me, press button below!",
        reply_markup=main_menu_keyboard
    )

    await bot.send_message(
        partner_user.tg_id,
        f"{message.from_user.full_name} has joined using your invite link!"
    )


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
