from sqlalchemy import select
from sqlalchemy.orm import declarative_base

from database.connector import db_conn
from settings import setting

Base = declarative_base()


async def init_db():
    print("Initializing database")
    db_conn.initialize(setting.async_db_url)


class Manager:
    connection = db_conn

    async def save(self):
        async with  self.connection.session as sess:
            sess.add(self)
            await sess.commit()
            await sess.refresh(self)
            return self

    @classmethod
    async def get_object_or_none(cls, session=None, **kwargs):
        async with (session or cls.connection.session) as sess:
            query = select(cls).filter_by(**kwargs)
            result = await sess.execute(query)
            if obj := result.scalar_one_or_none():
                return obj

    async def delete(self, session=None) -> bool:
        async with (session or self.connection.session) as sess:
            sess.delete(self)
            await session.commit()
            return True
