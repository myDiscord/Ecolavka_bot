from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def ikb_account_uz(data) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    data.sort(key=lambda x: x.get('updated_at'), reverse=True)

    if isinstance(data, list):
        for index, entry in enumerate(data):
            updated_at = entry.get('updated_at')
            if updated_at:
                builder.button(text=f'{updated_at}', callback_data=f'order_{index}')

        builder.button(text='🚪Asosiy menyu', callback_data='start')

        builder.adjust(*([1] * len(data)), 1)

    else:
        builder.button(text=f'{data}', callback_data=f'order_{data}')

        builder.button(text='🚪Asosiy menyu', callback_data='start')

        builder.adjust(1, 1)
    return builder.as_markup()


def ikb_account_2_uz() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='🔙 Orqaga', callback_data=f'account')
    builder.button(text='🚪Asosiy menyu', callback_data='start')

    builder.adjust(2)
    return builder.as_markup()
