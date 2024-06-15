import asyncio
import logging

from database.base import Base
from database.connector import db_conn
from loader import bot, dp
import handlers

logger = logging.getLogger(__name__)


async def init_db():
    print("Initializing database")
    db_conn.initialize("sqlite+aiosqlite:///db.sqlite3")

    async with db_conn.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main() -> None:
    await init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Starting bot...")
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
