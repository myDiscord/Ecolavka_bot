from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):

    news = State()
    account = State()

    brand = State()
    lines = State()
    category = State()
    products = State()
    product = State()
    cart = State()

    name_ru = State()
    phone_ru = State()
    geo_ru = State()

    name_uz = State()
    phone_uz = State()
    geo_uz = State()
