from pytz import timezone
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, func, ForeignKey, DECIMAL, UniqueConstraint
from sqlalchemy.orm import declared_attr, relationship
from sqlalchemy_file import ImageField

from src.config_reader import settings
from .base import Base

timezone = timezone(settings.timezone)


class TimeStampedMixin:
    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now())

    @declared_attr
    def updated_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class User(Base, TimeStampedMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, unique=True)
    tg_username = Column(String(length=32), unique=True)
    tg_first_name = Column(String(length=64))
    tg_language_code = Column(String(length=6))

    expenses = relationship("Expense", back_populates="user", cascade="all, delete-orphan")


class Expense(Base, TimeStampedMixin):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    user_tg_id = Column(ForeignKey('users.tg_id', ondelete="CASCADE"), nullable=False)
    amount = Column(DECIMAL(8, 2), nullable=False)
    category = Column(String(length=64))
    comment = Column(String(length=255))
    payment_type = Column(String(length=32), nullable=False)

    receipt = Column(ImageField(), nullable=True)

    user = relationship("User", back_populates="expenses")


class UserRelationship(Base):
    __tablename__ = "user_relationships"

    id = Column(Integer, primary_key=True)
    initiating_user_tg_id = Column(ForeignKey('users.tg_id', ondelete="CASCADE"), nullable=False)
    partner_user_tg_id = Column(ForeignKey('users.tg_id', ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        UniqueConstraint('initiating_user_tg_id', 'partner_user_tg_id', name='unique_relationship'),
        # TODO: Check reversed record
    )

    initiating_user = relationship(
        "User",
        foreign_keys=[initiating_user_tg_id],
    )
    partner_user = relationship(
        "User",
        foreign_keys=[partner_user_tg_id],
    )
