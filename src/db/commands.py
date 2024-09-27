from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from db import User
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
        category: str = None,
        comment: str = None,
):
    await session.merge(
        Expense(
            user_tg_id=user_id,
            amount=amount,
            category=category,
            comment=comment
        )
    )
    await session.commit()
