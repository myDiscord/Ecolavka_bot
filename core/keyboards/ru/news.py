from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def rkb_news(news: list, language: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    n = len(news)

    builder.button(text='📖 Главное меню')

    for post in news:
        builder.button(text=f'{post[f"title_{language}"]}')

    builder.adjust(*[1] * n, 1)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def rkb_post() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🔙 Назад')
    builder.button(text='📖 Главное меню')

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)
