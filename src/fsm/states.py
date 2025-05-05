from aiogram.fsm.state import StatesGroup, State


class CreatingChar(StatesGroup):
    Name = State()
    StartContext = State()
