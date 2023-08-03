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

    in_cart = State()

    name = State()
    phone = State()
    geo = State()
