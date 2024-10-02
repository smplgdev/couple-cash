from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from config_reader import config

Base = declarative_base()

engine = create_async_engine(
    config.db_url,
)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
