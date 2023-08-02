from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def ikb_name() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='🔙 Назад', callback_data=f'cart_ru')
    builder.button(text='🚪Главное меню', callback_data='start')

    builder.adjust(2)
    return builder.as_markup()


def ikb_pay() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Click', callback_data='CLICK')
    builder.button(text='Paycom', callback_data='PAYCOM')
    builder.button(text='Наличными курьеру', callback_data='CASH')

    builder.button(text='🔙 Назад', callback_data=f'cart_ru')
    builder.button(text='🚪Главное меню', callback_data='start')

    builder.adjust(2, 1, 2)
    return builder.as_markup()
