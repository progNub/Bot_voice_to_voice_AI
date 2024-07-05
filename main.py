import asyncio
import logging

from database.base import init_db
from loader import bot, dp
from handlers import handlers

logger = logging.getLogger(__name__)


async def main() -> None:
    await init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
