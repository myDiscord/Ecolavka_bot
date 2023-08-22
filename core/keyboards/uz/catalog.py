from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def rkb_brands_uz(brands) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    n = len(brands)
    for brand in brands:
        builder.button(text=f'{brand["title"]}')

    builder.button(text='🚪Asosiy menyu')

    builder.adjust(* [1] * n, 1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def rkb_lines_uz(brand_lines) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🔙 Orqaga')
    builder.button(text='🚪Asosiy menyu')

    n = len(brand_lines)
    for brand_line in brand_lines:
        builder.button(text=f'{brand_line["title"].split(" ")[-1].capitalize()}')

    builder.adjust(2, * [2] * n)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def rkb_categories_uz(categories, language) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🔙 Orqaga')
    builder.button(text='🚪Asosiy menyu')

    n = len(categories)
    for category in categories:
        builder.button(text=f'{category[f"title_{language}"].split(" ")[-1].capitalize()}')

    builder.adjust(2, * [2] * n)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def rkb_subcategories_uz(subcategories, language) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🔙 Orqaga')
    builder.button(text='🚪Asosiy menyu')

    n = len(subcategories)
    for subcategory in subcategories:
        builder.button(text=subcategory[f'title_{language}'])

    builder.adjust(2, * [2] * n)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def rkb_products_uz(products, language) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🔙 Orqaga')
    builder.button(text='📖 Asosiy menyu')

    n = len(products)
    for product in products:
        text = product[f'title_{language}']
        # if text.lower.strtswith('mayeri all-care'):
        #     text = text.replace('mayeri all-care', '', 1)
        # elif text.lower.strtswith('mayeri sensitive'):
        #     text = text.replace('mayeri sensitive', '', 1)
        builder.button(text=text)

    builder.adjust(2, * [1] * n)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def rkb_care_uz(products, language) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🗂 Katalogi')
    builder.button(text='📖 Asosiy menyu')

    n = len(products)
    for product in products:
        text = product[f'title_{language}'].lower()
        text = text.replace('mayeri all-care', '', 1)
        text = text.replace('mayeri sensitive', '', 1)
        builder.button(text=text.capitalize())

    builder.adjust(2, * [1] * n)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def rkb_product_uz() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text="✅ Savatga qo'shish")
    builder.button(text='🔙 Orqaga')
    builder.button(text='📖 Asosiy menyu')

    builder.adjust(1, 2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def rkb_product_in_cart_uz() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🧺 Savat')

    builder.button(text='🔙 Orqaga')
    builder.button(text='📖 Asosiy menyu')

    builder.adjust(1, 2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
