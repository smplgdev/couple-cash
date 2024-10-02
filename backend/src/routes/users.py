from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
from db import models
from db.get_db import get_db

router = APIRouter(prefix='/telegram-users')


@router.get('/{user_tg_id}')
async def get_user_by_id(user_tg_id: int, db: AsyncSession = Depends(get_db)) -> schemas.UserResponse:
    stmt = (
        select(models.User).
        where(models.User.tg_id == user_tg_id)
    )

    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    return user


@router.get('/{user_tg_id}/expenses', response_model=list[schemas.ExpenseResponse])
async def get_expenses(user_tg_id: int, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(models.Expense).
        filter(models.Expense.user_tg_id == user_tg_id)
    )
    result = await db.execute(stmt)
    expenses = result.scalars().all()
    return expenses
