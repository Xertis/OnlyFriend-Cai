from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from datetime import datetime
from src.logic.ai import AiSession
from src.constants import Constants
from src.sql.api import DB
from src.utils import translate
from aiogram.exceptions import TelegramBadRequest


class Ai:
    def __init__(self):
        self.router = Router()
        self.db = DB()
        self.router.message(
            lambda message: not message.text.startswith('/'),
            StateFilter(None)
        )(self.process)

    async def process(self, message: Message):
        owner = self.db.users.get(message.from_user.id)
        char = self.db.chars.get_by_id(character_id=owner.current_char)

        if not char:
            await message.answer("Не выбран персонаж, введите команду /new для создания персонажа, и /feed, чтобы его выбрать")
            return

        question = ''
        if len(char.context) > 0:
            question = char.context
        else:
            question = await translate(message=char.start_context, src="ru", dest="en") + char.context

        session = AiSession(model=Constants.NN_MODEL, context=question)
        try:
            answer = await session.ask(message=message.text)

            await message.answer(
                answer,
                parse_mode="Markdown"
            )
        except TelegramBadRequest:
            await message.answer(answer)
        except Exception as e:
            await message.answer(f'ОШИБКА: {e}')

        self.db.chars.update_context(char.id, session.context)
        owner.last_upd = datetime.now()
        self.db.session.commit()
