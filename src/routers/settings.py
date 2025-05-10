from aiogram import Router, F, types, Bot
from aiogram.types import Message
from aiogram.filters import Command
from src.logic.ai import AiSession
from src.constants import Constants
from aiogram.fsm.context import FSMContext
from src.fsm.states import CreatingChar
from src.sql.api import DB
from src.utils import BuildInlineButtons


class Settings:
    def __init__(self):
        self.router = Router()
        self.db = DB()
        self.router.message(Command("feed"))(self.characters_feed)

        self.router.message(Command("new"))(self.new_char_start)
        self.router.message(CreatingChar.Name)(self.new_char_name)
        self.router.message(CreatingChar.StartContext)(self.new_char_context)

        self.router.callback_query(self.char_del_cheaker)(self.del_char)
        self.router.callback_query(self.char_set_cheaker)(self.set_char)

    @staticmethod
    async def char_set_cheaker(callback):
        return callback.data.startswith("char.set")
    
    @staticmethod
    async def char_del_cheaker(callback):
        return callback.data.startswith("char.del")
    
    async def del_char(
        self,
        callback_query: 
        types.CallbackQuery, 
        bot: Bot
    ):
        
        char_id = int(callback_query.data.split(':')[-1])

        self.db.chars.delete(character_id=char_id)

        message = callback_query.message
        await bot.delete_message(message.chat.id, message.message_id)
        await callback_query.answer()

    async def set_char(
        self,
        callback_query: 
        types.CallbackQuery, 
    ):
        
        char_id = int(callback_query.data.split(':')[-1])
        owner = self.db.users.get(callback_query.from_user.id)

        self.db.users.set_char(owner, char_id)

        await callback_query.message.answer("Новый персонаж выбран")
        await callback_query.answer()


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
            name=name,
            start_context=context,
            owner=self.db.users.get(tg_id=tg_id).id
        )

        await message.answer("Урарцаркраукраукр, наконец-то, новый персонаж создан")
        await state.clear()
    
    async def characters_feed(
        self,
        message: Message,
    ):  
        owner = self.db.users.get(message.from_user.id)
        characters_data = self.db.chars.get_by_owner(owner_id=owner.id)

        await message.answer("Ваши персонажи:", parse_mode="Markdown")

        for char in characters_data:

            caption = f'''
*Имя*: {char.name}
*Стартовый контекст*: {char.start_context}
*Размер переписки*: {len(char.context.split())} слов
'''
            keyboard = await BuildInlineButtons([
                [["Использовать", f"char.set:{char.id}"]],
                [["Удалить", f"char.del:{char.id}"]]
            ])

            if char.img_id:
                await message.answer_photo(
                    photo=char.img_id,
                    caption=caption,
                    parse_mode="Markdown",
                    reply_markup=keyboard
                )

            else:
                await message.answer(
                    caption,
                    parse_mode="Markdown",
                    reply_markup=keyboard
                )