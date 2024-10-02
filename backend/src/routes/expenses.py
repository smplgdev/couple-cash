from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.get_db import get_db
from db import models
import schemas

router = APIRouter(prefix='/expenses')


@router.get("/", response_model=list[schemas.ExpenseResponse])
async def get_expenses(user_tg_id: list[int] = Query(default=[]), db: AsyncSession = Depends(get_db)):
    stmt = select(models.Expense)
    if user_tg_id:
        stmt = stmt.filter(models.Expense.user_tg_id.in_(user_tg_id))  # type: ignore
    result = await db.execute(stmt)
    expenses = result.scalars().all()
    return expenses


@router.post("/", response_model=schemas.ExpenseResponse)
async def create_expense(expense: schemas.ExpenseCreate, db: AsyncSession = Depends(get_db)):
    db_expense = models.Expense(**expense.model_dump())
    db.add(db_expense)
    await db.commit()
    await db.refresh(db_expense)
    return db_expense


@router.get("/{expense_id}", response_model=Optional[schemas.ExpenseResponse])
async def get_expense_by_id(expense_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Expense).filter(models.Expense.id == expense_id))
    expense = result.scalar_one_or_none()
    return expense
