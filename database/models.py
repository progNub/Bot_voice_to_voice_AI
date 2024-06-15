from sqlalchemy import Column, Integer, String
from typing import Self
from database.base import Base
from database.connector import db_conn

from sqlalchemy import select


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    thread_id = Column(String(255))

    def __str__(self):
        return f"User <id:{self.id}, id_tel:{self.id_user_assistant}, id_thread:{self.thread_id}>"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    async def is_user_exists(telegram_id):
        async with db_conn.session as session:
            query = select(User).where(User.telegram_id == telegram_id)

            result = await session.execute(query)
            return result.scalar()

    @staticmethod
    async def get_user(telegram_id):
        async with db_conn.session as session:
            query = select(User).where(User.telegram_id == telegram_id)
            user = await session.execute(query)
            return user.scalar_one_or_none()

    async def save(self) -> Self:
        async with db_conn.session as session:
            session.add(self)
            await session.commit()
            await session.refresh(self)
        return self

    async def delete(self):
        async with db_conn.session as session:
            session.delete(self)
            await session.commit()

