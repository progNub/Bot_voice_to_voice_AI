from typing import Self

from sqlalchemy import select, Sequence
from sqlalchemy.orm import declarative_base

from database.connector import db_conn
from settings import setting

Base = declarative_base()


async def init_db():
    print("Initializing database")
    db_conn.initialize(setting.async_db_url)


class Manager:

    async def save(cls) -> "Self":
        async with db_conn.session as session:
            session.add(cls)
            await session.commit()
            await session.refresh(cls)
        return cls

    @classmethod
    async def get(cls, **kwargs) -> Self | None:
        async with db_conn.session as session:
            query = select(cls)
            for key, value in kwargs.items():
                if not hasattr(cls, key):
                    raise AttributeError(f"Class {cls.__name__} has no attribute '{key}'")
                query = query.where(getattr(cls, key) == value)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            return result

    @classmethod
    async def all(cls) -> Sequence[Self]:
        async with db_conn.session as session:
            result = await session.execute(select(cls))
            return result.scalars().all()

    async def delete(self):
        async with db_conn.session as session:
            await session.delete(self)
            await session.commit()
            return True
