from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def rkb_account(data) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    if isinstance(data, list):

        data.sort(key=lambda x: x.get('updated_at'), reverse=True)

        builder.button(text='📖 Главное меню')
        builder.button(text='🇺🇿 Сменить язык')

        for index, entry in enumerate(data):
            updated_at = entry.get('updated_at')
            if updated_at:
                builder.button(text=f'Заказ за: {updated_at}')

        builder.adjust(2, *([1] * len(data)))

    else:
        builder.button(text=f'Заказ за: {data}')

        builder.button(text='📖 Главное меню')
        builder.button(text='🇺🇿 Сменить язык')

        builder.adjust(1, 2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def rkb_account_2() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🔙 Назад')
    builder.button(text='📖 Главное меню')

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)
