import asyncio
import logging

from aiogram import Bot, Dispatcher
from src.constants import Constants

bot = Bot(token=Constants.TOKEN)
dp = Dispatcher()

async def main():
    # dp.include_routers()
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())