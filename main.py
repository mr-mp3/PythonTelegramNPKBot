import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import start, help, menu, search, filters, movies
from services.database import init_db


async def main():
    logging.basicConfig(level=logging.INFO)

    init_db()

    bot = Bot(
        BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(menu.router)
    dp.include_router(filters.router)
    dp.include_router(search.router)
    dp.include_router(movies.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
