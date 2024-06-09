import asyncio
import logging
import handlers

from loader import bot, dp

logger = logging.getLogger(__name__)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Starting bot...")
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
