from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from src.logic.ai import AiSession
from src.constants import Constants
from src.sql.api import DB


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

        session = AiSession(model=Constants.NN_MODEL, context=char.start_context + char.context)
        try:
            await message.answer(
                await session.ask(message=message.text),
                parse_mode="Markdown"
            )
        except Exception as e:
            await message.answer(f'ОШИБКА: {e}')

        self.db.chars.update_context(char.id, session.context)
