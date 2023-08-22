from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def rkb_news_uz(news: list, language: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    n = len(news)

    builder.button(text='📖 Asosiy menyu')

    for post in news:
        builder.button(text=f'{post[f"title_{language}"]}')

    builder.adjust(*[1] * n, 1)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def rkb_post_uz() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🔙 Orqaga')
    builder.button(text='📖 Asosiy menyu')

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
