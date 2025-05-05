from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from src.logic.ai import AiSession
from src.constants import Constants


class Ai:
    def __init__(self):
        self.router = Router()
        self.session = AiSession(model=Constants.NN_MODEL)
        self.router.message(
            lambda message: not message.text.startswith('/'),
            StateFilter(None)
        )(self.process)

    async def process(self, message: Message):
        try:
            await message.answer(
                await self.session.ask(message=message.text),
                parse_mode="Markdown"
            )
        except Exception as e:
            await message.answer(f'ОШИБКА: {e}')
