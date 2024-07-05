import asyncio
import logging

from loader import bot, dp
from handlers import handlers

logger = logging.getLogger(__name__)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
