from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def rkb_brands(brands) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    n = len(brands)
    for brand in brands:
        builder.button(text=f'{brand["title"]}')

    builder.button(text='🚪Главное меню')

    builder.adjust(* [1] * n, 1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def rkb_lines(brand_lines) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🔙 Назад')
    builder.button(text='🚪Главное меню')

    n = len(brand_lines)
    for brand_line in brand_lines:
        builder.button(text=f'{brand_line["title"].split(" ")[-1]}')

    builder.adjust(2, * [2] * n)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def rkb_categories(categories, language) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🔙 Назад')
    builder.button(text='🚪Главное меню')

    n = len(categories)
    for category in categories:
        builder.button(text=f'{category[f"title_{language}"].split(" ")[-1]}')

    builder.adjust(2, * [2] * n)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def rkb_subcategories(subcategories, language) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🔙 Назад')
    builder.button(text='🚪Главное меню')

    n = len(subcategories)
    for subcategory in subcategories:
        builder.button(text=subcategory[f'title_{language}'])

    builder.adjust(2, * [2] * n)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def rkb_products(products, language) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🔙 Назад')
    builder.button(text='🚪Главное меню')

    n = len(products)
    for product in products:
        text = product[f'title_{language}']
        # if text.lower.strtswith('mayeri all-care'):
        #     text = text.replace('mayeri all-care', '', 1)
        # elif text.lower.strtswith('mayeri sensitive'):
        #     text = text.replace('mayeri sensitive', '', 1)
        builder.button(text=text)

    builder.adjust(2, * [1] * n)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def rkb_care(products, language) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🗂 Каталог')
    builder.button(text='🚪Главное меню')

    n = len(products)
    for product in products:
        text = product[f'title_{language}'].lower()
        text = text.replace('mayeri all-care', '', 1)
        text = text.replace('mayeri sensitive', '', 1)
        builder.button(text=text)

    builder.adjust(2, * [1] * n)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def rkb_product() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='✅ Добавить в корзину')
    builder.button(text='🔙 Назад')
    builder.button(text='🚪Главное меню')

    builder.adjust(1, 2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def rkb_product_in_cart() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🧺 Корзина')

    builder.button(text='🔙 Назад')
    builder.button(text='🚪Главное меню')

    builder.adjust(1, 2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)
