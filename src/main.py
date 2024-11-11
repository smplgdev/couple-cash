import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.handlers.commands import start
from src.handlers.messages import count_difference, monthly_expenses
from src.handlers.messages import expense, non_linked_users, recent_expenses
from src.middlewares.db import DbSessionMiddleware
from src.config_reader import settings
from src.utils.configure_storage import configure_storage
from src.utils.setup_logging import setup_logging


logger = logging.getLogger(__name__)


async def main():
    setup_logging()

    configure_storage()

    engine = create_async_engine(url=str(settings.database_uri), echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(settings.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode="HTML"))

    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))

    dp.include_router(start.router)
    dp.include_router(non_linked_users.router)

    dp.include_router(expense.router)
    dp.include_router(recent_expenses.router)
    dp.include_router(count_difference.router)
    dp.include_router(monthly_expenses.router)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
