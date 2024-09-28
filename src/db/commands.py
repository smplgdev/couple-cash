from sqlalchemy import select, exists
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import DataError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.operators import or_

from db import User, UserRelationship
from db.models import Expense


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


async def add_expense(
        session: AsyncSession,
        user_id: int,
        amount: float,
        category: str,
        comment: str,
        payment_type: str
) -> bool:
    await session.merge(
        Expense(
            user_tg_id=user_id,
            amount=amount,
            category=category,
            comment=comment,
            payment_type=payment_type
        )
    )
    try:
        await session.commit()
    except DataError:
        return False

    return True


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
