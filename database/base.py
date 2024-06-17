from sqlalchemy.orm import declarative_base

from database.connector import db_conn

Base = declarative_base()


async def init_db():
    print("Initializing database")
    db_conn.initialize("sqlite+aiosqlite:///db.sqlite3")

    async with db_conn.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)