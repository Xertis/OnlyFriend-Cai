import asyncio
import logging

from aiogram import Bot, Dispatcher
from src.constants import Constants

from src.routers.ai import Ai

bot = Bot(token=Constants.TOKEN)
dp = Dispatcher()

async def main():
    dp.include_routers(Ai().router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())