from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.settings import settings


def ikb_connection() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Чат с менеджером', url=f't.me/{settings.contacts.manager}')
    builder.button(text='🚪Главное меню', callback_data='start')

    builder.adjust(1, 1, 1)
    return builder.as_markup()
