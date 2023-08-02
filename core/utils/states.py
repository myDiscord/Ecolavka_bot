from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):

    name_ru = State()
    phone_ru = State()
    geo_ru = State()

    name_uz = State()
    phone_uz = State()
    geo_uz = State()
