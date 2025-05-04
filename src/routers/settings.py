from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.filters import Command
from src.logic.ai import AiSession
from src.constants import Constants
from aiogram.fsm.context import FSMContext
from src.fsm.states import CreatingChar
from src.sql.api import DB


class Settings:
    def __init__(self):
        self.router = Router()
        self.db = DB()
        self.router.message(Command("config"))

        self.router.message(Command("new"))(self.new_char_start)
        self.router.message(CreatingChar.Name)(self.new_char_name)
        self.router.message(CreatingChar.StartContext)(self.new_char_context)

    async def new_char_start(
            self,
            message: Message,
            state: FSMContext
        ):

        await state.set_state(CreatingChar.Name)
        await message.answer("Отправьте имя нового персонажа.", parse_mode="Markdown")

    async def new_char_name(
            self,
            message: Message,
            state: FSMContext
        ):
        
        name = message.text
        if self.db.chars.has(owner_tg_id=message.from_user.id, name=name):
            await message.answer("Неверное имя персонажа/такое имя персонажа уже занято.")
            await state.clear()
            return
        
        await message.answer("Отправьте описание персонажа, сделайте его не менее, чем на 10 слов.")
        await state.update_data(name=name)
        await state.set_state(CreatingChar.StartContext)

    async def new_char_context(
            self,
            message: Message,
            state: FSMContext
        ):
        data = await state.get_data()

        tg_id = message.from_user.id
        context = message.text
        name = data["name"]

        if len(context.split()) < 10:
            await message.answer("Слишком мало информации о вашем персонаже, попробуйте сделать его описание больше 10 слов.")
            return
        
        self.db.chars.add(
            name = name,
            start_context=context,
            owner=self.db.users.get(tg_id=tg_id).id
        )

        await message.answer("Урарцаркраукраукр, наконец-то, новый персонаж создан")
        await state.clear()
        
