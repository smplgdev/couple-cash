from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from db.commands import is_user_linked


class LinkedUsersFilter(BaseFilter):
    async def __call__(self, message: Message, session: AsyncSession):
        return await is_user_linked(session, message.from_user.id)
