from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def rkb_account_uz(data) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    if isinstance(data, list):

        data.sort(key=lambda x: x.get('updated_at'), reverse=True)

        builder.button(text='🚪Asosiy menyu')

        for index, entry in enumerate(data):
            updated_at = entry.get('updated_at')
            if updated_at:
                builder.button(text=f'{updated_at}')

        builder.adjust(*([1] * len(data)), 1)

    else:
        builder.button(text=f'{data}')

        builder.button(text='🚪Asosiy menyu')

        builder.adjust(1, 1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def rkb_account_2_uz() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🔙 Orqaga')
    builder.button(text='🚪Asosiy menyu')

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
