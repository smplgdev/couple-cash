from io import BytesIO
from datetime import datetime

import aiogram.exceptions
from aiogram import Router, F, Bot
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.markdown import hcode
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_file import File
from sqlalchemy_file.storage import StorageManager

from src.handlers.messages.count_difference import PAY_FOR_MY_PARTNER, SPLIT_THE_EXPENSE
from src.keyboards import payment_type_keyboard, main_menu_keyboard, category_keyboard, ADD_EXPENSE
from src.db import UserRelationship
from src.db.commands import create_expense
from src.filters.linked_users import LinkedUsersFilter
from src.notion.api import create_notion_db_record
from src.schemas import ExpenseCreate


class ExpenseStates(StatesGroup):
    amount = State()
    category = State()
    comment = State()
    payment_type = State()


router = Router()


@router.message(LinkedUsersFilter(), F.text == ADD_EXPENSE)
async def expense_handler(message: Message, state: FSMContext):
    await state.set_state(ExpenseStates.amount)
    await message.answer("Please, specify the amount of the expense:")


@router.message(LinkedUsersFilter(), ExpenseStates.amount)
async def amount_handler(message: Message, state: FSMContext):
    amount_as_text = message.text.replace(",", ".")

    try:
        amount = float(amount_as_text)
    except ValueError:
        await message.answer("Invalid amount. Please, specify the amount of the expense:")
        return

    await state.update_data(amount=amount)

    await state.set_state(ExpenseStates.category)
    await message.answer("Please, specify the category of the expense:", reply_markup=category_keyboard)


@router.message(LinkedUsersFilter(), ExpenseStates.category)
async def category_handler(message: Message, state: FSMContext):
    category = message.text
    await state.update_data(category=category)

    await state.set_state(ExpenseStates.comment)
    await message.answer("Please, specify the comment for the expense AND/OR upload the receipt (If necessary):")


@router.message(LinkedUsersFilter(), ExpenseStates.comment, F.content_type == ContentType.PHOTO)
async def receipt_handler(message: Message, state: FSMContext, bot: Bot):
    file_info = await bot.get_file(message.photo[-1].file_id)
    file_data = await bot.download_file(file_info.file_path)
    image_bytes = BytesIO(file_data.read())
    image_bytes.seek(0)
    await state.update_data(image_bytes=image_bytes)
    await ask_type_of_expense(message, state)


@router.message(LinkedUsersFilter(), ExpenseStates.comment)
async def comment_handler(message: Message, state: FSMContext):
    comment = message.text
    await state.update_data(comment=comment)
    await ask_type_of_expense(message, state)


async def ask_type_of_expense(message: Message, state: FSMContext):
    await state.set_state(ExpenseStates.payment_type)
    await message.answer(
        "And the last step...\n\nPlease, specify the payment type of the expense:",
        reply_markup=payment_type_keyboard
    )


@router.message(LinkedUsersFilter(), ExpenseStates.payment_type)
async def payment_type_handler(message: Message, state: FSMContext, session: AsyncSession, relationship: UserRelationship, bot: Bot):
    payment_type = message.text
    await state.update_data(payment_type=payment_type)

    data = await state.get_data()
    amount = data["amount"]
    category = data["category"]
    comment = data.get("comment", None)
    image_bytes: BytesIO | None = data.get("image_bytes", None)

    expense = ExpenseCreate(
        user_tg_id=message.from_user.id,
        amount=amount,
        category=category,
        comment=comment,
        payment_type=payment_type,
    )

    create_notion_db_record(expense, purchaser_name=message.from_user.first_name)

    # Add expense to the database
    await create_expense(
        session,
        **expense.dict(),
        receipt=File(content=image_bytes, content_type="image/jpeg") if image_bytes else None
    )

    await send_notification_to_partner(
        message=message,
        payment_type=payment_type,
        amount=amount,
        relationship=relationship,
        bot=bot
    )

    await state.clear()
    await message.answer(f"Expense {hcode(f"{amount} €".replace(".", ","))} has been added with category {hcode(category)} and comment {hcode(comment)}!",
                         reply_markup=main_menu_keyboard)


async def send_notification_to_partner(
        message: Message,
        payment_type: str,
        amount: float,
        relationship: UserRelationship,
        bot: Bot) -> None:
    if payment_type in (PAY_FOR_MY_PARTNER, SPLIT_THE_EXPENSE):
        if message.from_user.id == relationship.initiating_user_tg_id:
            partner_id = relationship.partner_user_tg_id
        else:
            partner_id = relationship.initiating_user_tg_id

        try:

            await bot.send_message(partner_id, f"New expense {hcode(f"{amount} €".replace(".", ","))} from {message.from_user.first_name} with category {hcode(category)} and comment {hcode(comment)}!")
        except aiogram.exceptions.TelegramNotFound:
            pass
