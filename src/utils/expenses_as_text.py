from typing import Sequence

from aiogram.utils.markdown import hbold

from src.db import Expense
from src.handlers.messages.count_difference import PAY_FOR_MYSELF, PAY_FOR_MY_PARTNER, SPLIT_THE_EXPENSE


def get_expenses_as_text(expenses: Sequence[Expense], user_tg_id: int) -> str:
    text_parts = list()
    spent: float = 0

    for expense in expenses:
        expense_spent = 0

        if any([
            expense.payment_type == PAY_FOR_MYSELF and expense.user_tg_id == user_tg_id,
            expense.payment_type == PAY_FOR_MY_PARTNER and expense.user_tg_id != user_tg_id
        ]):
            expense_spent = expense.amount
        elif expense.payment_type == SPLIT_THE_EXPENSE:
            expense_spent = expense.amount / 2

        spent += expense_spent
        sum_text = str(round(expense_spent, 2)).replace(".", ",") + " €"
        if expense_spent != 0:
            text_parts.append(f"\n{expense.user.tg_first_name} [{expense.created_at.strftime("%d.%m at %H:%M")}]\n{sum_text}\n{expense.category}\n{expense.comment}")

    text_parts.append(hbold(f"\nYou spent in this period in total: {str(round(spent, 2)).replace(".", ",")} €"))
    return "\n".join(text_parts)
