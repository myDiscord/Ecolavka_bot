import math

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def ikb_news_uz(news: list, language: str, current_page: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    buttons_per_page = 10
    start_index = current_page * buttons_per_page
    end_index = min(start_index + buttons_per_page, len(news))
    buttons_to_show = news[start_index:end_index]
    n = min(end_index - start_index, buttons_per_page)

    for post in buttons_to_show:
        builder.button(text=f'{post[f"title_{language}"]}', callback_data=f'post_{current_page}_{post["id"]}')

    if current_page == 0:
        b_back = '-'
        callback_back = '+'
    else:
        b_back = '⬅️ Orqaga'
        callback_back = f'news_{current_page - 1}'
    builder.button(text=b_back, callback_data=callback_back)

    builder.button(text=f'{current_page + 1} / {math.ceil(len(news) / buttons_per_page)}',
                   callback_data=f'list_uz_{current_page + 1}_{math.ceil(len(news) / buttons_per_page)}')

    if end_index < len(news):
        b_next = 'Keyingi ➡️'
        callback_next = f'news_{current_page + 1}'
    else:
        b_next = '-'
        callback_next = '+'
    builder.button(text=b_next, callback_data=callback_next)

    builder.button(text='🚪Asosiy menyu', callback_data='start')

    builder.adjust(*[1] * n, 3, 1)

    return builder.as_markup()


def ikb_post_uz(current_page: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='🔙 Orqaga', callback_data=f'news_{current_page}')
    builder.button(text='🚪Asosiy menyu', callback_data='start')

    builder.adjust(2)
    return builder.as_markup()
