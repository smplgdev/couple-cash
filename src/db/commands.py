from sqlalchemy import select, distinct
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
    # TODO: Rewrite this with exists()

    stmt = (
        select(UserRelationship).
        filter(
            or_(
                UserRelationship.initiating_user_tg_id == tg_id,
                UserRelationship.partner_user_tg_id == tg_id,
            )
        )
    )

    is_exists = await session.execute(stmt)
    return bool(is_exists.scalar_one_or_none())


async def select_last_categories_of_user(session: AsyncSession, user_tg_id: int, n: int = 5) -> list[str]:
    stmt = (
        select(Expense.category).
        where(Expense.user_tg_id == user_tg_id).
        order_by(Expense.created_at.desc()).
        limit(n)
    )

    result = await session.execute(stmt)
    return list(set(row[0] for row in result.all()))
