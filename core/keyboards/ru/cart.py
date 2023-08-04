from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def rkb_cart(products) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='💳 Заказать')
    builder.button(text='🚪Главное меню')

    n = len(products)
    for product in products:
        builder.button(text=product)

    builder.adjust(2, * [1] * n)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def rkb_cart_product(number: int) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    if number == 1:
        builder.button(text='➕️больше')
        builder.button(text='✖️удалить товар')

        builder.button(text='🔙 Назад')
        builder.button(text='🚪Главное меню')

        builder.adjust(1, 1, 2)

    else:
        builder.button(text='➖️меньше')
        builder.button(text='➕️больше')
        builder.button(text='✖️удалить товар')

        builder.button(text='🔙 Назад')
        builder.button(text='🚪Главное меню')

        builder.adjust(2, 1, 2)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
