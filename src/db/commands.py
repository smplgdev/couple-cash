from datetime import date, timedelta

from sqlalchemy import select, exists, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import DataError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.operators import or_, and_

from .models import Expense, User, UserRelationship
from src.schemas import ExpenseCreate


async def create_or_update_user(
        session: AsyncSession,
        tg_id: int,
        tg_username: str,
        tg_first_name: str,
        tg_language_code: str,
        return_user: bool = True
) -> User | None:

    stmt = (
        insert(User).
        values(
            tg_id=tg_id,
            tg_username=tg_username,
            tg_first_name=tg_first_name,
            tg_language_code=tg_language_code
        ).
        on_conflict_do_update(
            constraint="users_tg_id_key",
            set_={
                User.tg_username: tg_username,
                User.tg_first_name: tg_first_name,
                User.tg_language_code: tg_language_code
            }
        )
    )

    if return_user:
        stmt = stmt.returning(User)

    result = await session.execute(stmt)
    await session.commit()
    return result.scalar_one_or_none()


async def get_user_or_none(session: AsyncSession, user_tg_id: int) -> User | None:
    stmt = (
        select(User).
        filter(User.tg_id == user_tg_id)
    )

    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def _create_expense(
        session: AsyncSession,
        expense: ExpenseCreate,
) -> Expense | None:
    expense_db = Expense(**expense.model_dump())
    await session.merge(expense_db)
    try:
        await session.commit()
    except DataError:
        return None
    return expense_db


async def create_expense(
    session: AsyncSession,
    **kwargs
):
    expense = Expense(**kwargs)
    session.add(expense)
    try:
        await session.commit()
    except DataError:
        return None
    return expense


async def is_user_linked(session: AsyncSession, tg_id: int) -> bool:
    stmt = (
        select(
            exists().
            where(
                or_(
                    UserRelationship.initiating_user_tg_id == tg_id,
                    UserRelationship.partner_user_tg_id == tg_id,
                )
            )
        )
    )

    is_exists = await session.execute(stmt)
    return is_exists.scalar()


async def create_user_relationship(session: AsyncSession, initiating_user_tg_id: int, partner_user_tg_id: int):
    await session.merge(
        UserRelationship(
            initiating_user_tg_id=initiating_user_tg_id,
            partner_user_tg_id=partner_user_tg_id
        )
    )
    await session.commit()


async def get_user_relationship(session: AsyncSession, tg_id: int) -> UserRelationship | None:
    stmt = (
        select(UserRelationship).
        where(
            or_(
                UserRelationship.initiating_user_tg_id == tg_id,
                UserRelationship.partner_user_tg_id == tg_id,
            )
        )
    )

    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def select_last_categories_of_user(session: AsyncSession, user_tg_id: int, n: int = 5) -> list[str]:
    # TODO: add partner's categories as well

    subq = (
        select(Expense.category, Expense.created_at).
        filter(Expense.user_tg_id == user_tg_id).
        order_by(Expense.created_at.desc()).
        subquery()
    )

    stmt = (
        select(subq.c.category).
        distinct().
        limit(n)
    )

    result = await session.execute(stmt)
    return list(set(row[0] for row in result.all()))


async def get_all_expenses(session: AsyncSession, relationship: UserRelationship):
    stmt = (
        select(Expense).
        where(
            or_(
                Expense.user_tg_id == relationship.partner_user_tg_id,
                Expense.user_tg_id == relationship.initiating_user_tg_id,
            )
        )
    )

    result = await session.execute(stmt)
    return result.scalars().all()


async def get_active_expense_months(session: AsyncSession, relationship: UserRelationship):
    stmt = (
        select(
            func.extract('year', Expense.created_at).label('year'),
            func.extract('month', Expense.created_at).label('month'),
        ).
        where(or_(
            Expense.user_tg_id == relationship.partner_user_tg_id,
            Expense.user_tg_id == relationship.initiating_user_tg_id,
        )).
        distinct().
        order_by('year', 'month')
    )

    result = await session.execute(stmt)

    # Convert results into a list of tuples
    active_months = [(int(row.year), int(row.month)) for row in result]

    return active_months


async def get_user_expenses_by_month(session: AsyncSession, month_any_date: date, relationship: UserRelationship):
    stmt = (
        select(Expense).
        where(
            or_(
                Expense.user_tg_id == relationship.partner_user_tg_id,
                Expense.user_tg_id == relationship.initiating_user_tg_id,
            )
        ).
        where(
            func.extract('year', Expense.created_at) == month_any_date.year,
            func.extract('month', Expense.created_at) == month_any_date.month
        ).
        options(selectinload(Expense.user))
    )

    result = await session.scalars(stmt)
    return result.all()


async def get_recent_expenses(session: AsyncSession, relationship: UserRelationship, period: int = 30):
    stmt = (
        select(Expense).
        where(
            and_(
                Expense.user_tg_id.in_([relationship.initiating_user_tg_id, relationship.partner_user_tg_id]),
                Expense.created_at >= date.today() - timedelta(days=period)
            )
        ).
        order_by(Expense.created_at.desc()).
        options(selectinload(Expense.user))
    )
    result = await session.execute(stmt)
    return result.scalars().all()
