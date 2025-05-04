import asyncio
import logging

from aiogram import Bot, Dispatcher
from src.constants import Constants
from aiogram.filters import Command
from aiogram.types import Message

from src.routers.ai import Ai
from src.routers.settings import Settings

from src.sql.api import DB

bot = Bot(token=Constants.TOKEN)
dp = Dispatcher()
db = DB()

@dp.message(Command("start"))
async def start(message: Message):
    tg_id = message.from_user.id
    if db.users.get(tg_id=tg_id) is None:
        db.users.add(tg_id=tg_id)

    await message.answer(Constants.START_MESSAGE, parse_mode="Markdown")

async def main():
    dp.include_routers(Ai().router, Settings().router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())