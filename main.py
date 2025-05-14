import asyncio
import logging

from io import BytesIO
from aiogram import Bot, Dispatcher
from src.constants import Constants
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile

from datetime import datetime, timedelta
from random import randint as rand

from src.sql.api import DB
from src.routers.ai import Ai
from src.utils import child_paint, BuildInlineButtons
from src.logic.ai import AiSession
from src.routers.settings import Settings
from apscheduler.schedulers.asyncio import AsyncIOScheduler

bot = Bot(token=Constants.TOKEN)
scheduler = AsyncIOScheduler()
dp = Dispatcher()
db = DB()


# Шедулеры

## Отправка случайных сообщений

async def send_rand_message():
    for user in db.users.get_all():
        user_id = user.tg_id

        char = db.chars.get_by_id(user.current_char)
        session = AiSession(Constants.NN_MODEL, translation=False)

        if not char:
            continue

        if user.last_upd and (datetime.now() - user.last_upd.replace(tzinfo=None)) < timedelta(minutes=5):
            continue

        if rand(0, 1) == 0:
            await bot.send_message(user_id, await session.ask(Constants.PLEA, False))
        else:
            buffer = BytesIO()
            img = await child_paint()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            photo = BufferedInputFile(buffer.getvalue(), filename='image.png')

            caption = await session.ask(Constants.PAINT, False)
            message = await bot.send_photo(user_id, photo=photo, caption=caption)
            photo_file_id = message.photo[-1].file_id
            d_img = db.imgs.add(photo_file_id)

            keyboard = await BuildInlineButtons([
                [["Поставить на аву", f"char.avatar:{d_img.id}:{char.id}"]]
            ])
            await bot.edit_message_reply_markup(
                chat_id=user_id,
                message_id=message.message_id,
                reply_markup=keyboard
            )

        user.last_upd = datetime.now()
        db.session.commit()


@dp.message(Command("start"))
async def start(message: Message):
    tg_id = message.from_user.id
    if db.users.get(tg_id=tg_id) is None:
        db.users.add(tg_id=tg_id)

    await message.answer(Constants.START_MESSAGE, parse_mode="Markdown")


async def main():
    scheduler.start()
    
    scheduler.add_job(
        send_rand_message,
        'interval',
        minutes=0.25,
        id='scheduled_message'
    )

    dp.include_routers(Ai().router, Settings().router)
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
