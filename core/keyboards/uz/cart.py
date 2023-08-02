from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def ikb_cart_uz(products, numbers, language) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    n = len(products)
    for index, product in enumerate(products):
        builder.button(text=f'{product[f"title_{language}"]}', callback_data=f'cart_{numbers[index]}_{product["id"]}')

    builder.button(text='💳 Buyurtma', callback_data=f'pay_uz')
    builder.button(text='🚪Asosiy menyu', callback_data='start_uz')

    builder.adjust(* [1] * n, 1, 1)
    return builder.as_markup()


def ikb_cart_product_uz(product_id: int, number: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if number == 1:
        builder.button(text="➕ko'proq", callback_data=f'cart_{number + 1}_{product_id}')
        builder.button(text="✖️mahsulotni o'chirish", callback_data=f'cart-del_{product_id}')

        builder.button(text='🔙 Orqaga', callback_data='cart_ru')
        builder.button(text='🚪Asosiy menyu', callback_data='start')

        builder.adjust(1, 1, 2)

    else:
        builder.button(text='➖kamroq', callback_data=f'cart_{number - 1}_{product_id}')
        builder.button(text="➕ko'proq", callback_data=f'cart_{number + 1}_{product_id}')
        builder.button(text="✖️mahsulotni o'chirish", callback_data=f'cart-del_{product_id}')

        builder.button(text='🔙 Orqaga', callback_data='cart_ru')
        builder.button(text='🚪Asosiy menyu', callback_data='start')

        builder.adjust(2, 1, 2)

    return builder.as_markup()
