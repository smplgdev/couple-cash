from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from db.commands import get_user_relationship


class LinkedUsersFilter(BaseFilter):
    async def __call__(self, message: Message, session: AsyncSession):
        relationship = await get_user_relationship(session, message.from_user.id)
        if not relationship:
            return False
        return {'relationship': relationship}
