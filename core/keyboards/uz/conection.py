from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def rkb_connection_uz() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🚪Asosiy menyu', callback_data='start')

    builder.adjust(1, 1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
