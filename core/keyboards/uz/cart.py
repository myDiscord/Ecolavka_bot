from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def rkb_cart_uz(products) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='💳 Buyurtma')
    builder.button(text='📖 Asosiy menyu')

    n = len(products)
    for product in products:
        builder.button(text=product)

    builder.adjust(2, * [1] * n)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def rkb_cart_product_uz(number: int) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    if number == 1:
        builder.button(text="➕ko'proq")
        builder.button(text="✖️mahsulotni o'chirish")

        builder.button(text='🔙 Orqaga')
        builder.button(text='📖 Asosiy menyu')

        builder.adjust(1, 1, 2)

    else:
        builder.button(text='➖kamroq')
        builder.button(text="➕ko'proq")
        builder.button(text="✖️mahsulotni o'chirish")

        builder.button(text='🔙 Orqaga')
        builder.button(text='📖 Asosiy menyu')

        builder.adjust(2, 1, 2)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
