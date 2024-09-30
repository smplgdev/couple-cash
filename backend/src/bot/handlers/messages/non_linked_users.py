from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link

from filters.linked_users import LinkedUsersFilter

router = Router()


@router.message(~LinkedUsersFilter())
async def not_linked_user_handler(message: Message, bot: Bot):
    link = await create_start_link(bot, payload=str(message.from_user.id))

    await message.answer(
        "You are not linked with your partner so far\n"
        f"\nSend this link to your partner to link with you:\n\n{link}",
    )
