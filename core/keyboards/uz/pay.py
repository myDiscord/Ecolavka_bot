from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def ikb_name_uz() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='🔙 Orqaga', callback_data=f'cart_ru')
    builder.button(text='🚪Asosiy menyu', callback_data='start')

    builder.adjust(2)
    return builder.as_markup()


def ikb_pay_uz() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Click', callback_data='CLICK_UZ')
    builder.button(text='Paycom', callback_data='PAYCOM_UZ')
    builder.button(text='Kuryerga naqd pul', callback_data='CASH_UZ')

    builder.button(text='🔙 Orqaga', callback_data=f'cart_ru')
    builder.button(text='🚪Asosiy meny', callback_data='start')

    builder.adjust(2, 1, 2)
    return builder.as_markup()
