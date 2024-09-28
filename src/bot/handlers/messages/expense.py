import aiogram.exceptions
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.markdown import hcode
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import payment_type_keyboard, main_menu_keyboard, category_keyboard, ADD_EXPENSE
from db import UserRelationship
from db.commands import add_expense, select_last_categories_of_user
from filters.linked_users import LinkedUsersFilter


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
async def amount_handler(message: Message, state: FSMContext, session: AsyncSession):
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
    await message.answer("Please, specify the comment for the expense:")


@router.message(LinkedUsersFilter(), ExpenseStates.comment)
async def comment_handler(message: Message, state: FSMContext):
    comment = message.text
    await state.update_data(comment=comment)

    await state.set_state(ExpenseStates.payment_type)
    await message.answer("And the last step...\n\nPlease, specify the payment type of the expense:",
                         reply_markup=payment_type_keyboard)


@router.message(LinkedUsersFilter(), ExpenseStates.payment_type)
async def payment_type_handler(message: Message, state: FSMContext, session: AsyncSession, relationship: UserRelationship, bot: Bot):
    payment_type = message.text
    await state.update_data(payment_type=payment_type)

    data = await state.get_data()
    amount = data["amount"]
    category = data["category"]
    comment = data["comment"]

    # Add expense to the database
    await add_expense(session, message.from_user.id, amount, category, comment, payment_type)

    if message.from_user.id == relationship.initiating_user_tg_id:
        partner_id = relationship.partner_user_tg_id
    else:
        partner_id = relationship.initiating_user_tg_id

    try:
        await bot.send_message(partner_id, f"New expense {hcode(f"{amount} €".replace(".", ","))} from {message.from_user.first_name} with category {hcode(category)} and comment {hcode(comment)}!")
    except aiogram.exceptions.TelegramNotFound:
        pass
    await state.clear()
    await message.answer(f"Expense {hcode(f"{amount} €".replace(".", ","))} has been added with category {hcode(category)} and comment {hcode(comment)}!",
                         reply_markup=main_menu_keyboard)
