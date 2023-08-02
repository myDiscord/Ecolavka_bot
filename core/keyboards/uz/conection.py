from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.settings import settings


def ikb_connection_uz() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Chat menejeri', url=f't.me/{settings.contacts.manager}')
    builder.button(text='🚪Asosiy menyu', callback_data='start')

    builder.adjust(1, 1, 1)
    return builder.as_markup()
