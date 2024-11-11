from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from src.config_reader import settings

Base = declarative_base()

engine = create_async_engine(
    str(settings.database_uri),
)
