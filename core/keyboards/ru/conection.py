from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def rkb_connection() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🚪Главное меню')

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
