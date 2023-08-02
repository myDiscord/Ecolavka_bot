from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def ikb_brands(brands) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    n = len(brands)
    for brand in brands:
        builder.button(text=f'{brand["title"]}', callback_data=f'ru_brand_{brand["id"]}')

    builder.button(text='🚪Главное меню', callback_data='start')

    builder.adjust(* [1] * n, 1)
    return builder.as_markup()


def ikb_lines(brand_lines) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    n = len(brand_lines)
    for brand_line in brand_lines:
        builder.button(text=f'{brand_line["title"]}',
                       callback_data=f'ru_brand-lines_{brand_line["title"]}_{brand_line["id"]}')

    builder.button(text='🔙 Назад', callback_data=f'Каталог продукции')
    builder.button(text='🚪Главное меню', callback_data='start')

    builder.adjust(* [1] * n, 2)
    return builder.as_markup()


def ikb_categories(categories, language, brand_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if isinstance(categories, list):
        n = len(categories)
        for category in categories:
            builder.button(text=f'{category[f"title_{language}"]}', callback_data=f'category_{category["id"]}')

        builder.button(text='🔙 Назад', callback_data=f'ru_brand_{brand_id}')
        builder.button(text='🚪Главное меню', callback_data='start')

        builder.adjust(* [1] * n, 2)

    else:
        builder.button(text=f'{categories[f"title_{language}"]}', callback_data=f'category_{categories["id"]}')

        builder.button(text='🔙 Назад', callback_data=f'ru_brand_{brand_id}')
        builder.button(text='🚪Главное меню', callback_data='start')

        builder.adjust(1, 2)

    return builder.as_markup()


def ikb_products(products, language, line_id, line_name) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    n = len(products)
    for product in products:
        product_title = product[f"title_{language}"].split(",")[:-1]
        button_text = ", ".join(product_title)
        builder.button(text=button_text, callback_data=f'product_1_{product["id"]}')

    builder.button(text='🔙 Назад', callback_data=f'ru_brand-lines_x {line_name}_{line_id}')
    builder.button(text='🚪Главное меню', callback_data='start')

    builder.adjust(* [1] * n, 2)
    return builder.as_markup()


def ikb_product(product_id, number: int, category_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='✅ Добавить в корзину', callback_data=f'cart-add_{number}_{product_id}')
    if number == 1:
        builder.button(text='➕️Больше', callback_data=f'product_{number + 1}_{product_id}')
        builder.button(text='🔙 Назад', callback_data=f'category_{category_id}')
        builder.button(text='🚪Главное меню', callback_data='start')

        builder.adjust(1, 1, 2)
    else:
        builder.button(text='➖️Меньше', callback_data=f'product_{number - 1}_{product_id}')
        builder.button(text='➕️Больше', callback_data=f'product_{number + 1}_{product_id}')

        builder.button(text='🔙 Назад', callback_data=f'category_{category_id}')
        builder.button(text='🚪Главное меню', callback_data='start')

        builder.adjust(1, 2, 2)
    return builder.as_markup()


def ikb_product_in_cart(category_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='🧺 Корзина', callback_data='cart_ru')

    builder.button(text='🔙 Назад', callback_data=f'category_{category_id}')
    builder.button(text='🚪Главное меню', callback_data='start')

    builder.adjust(1, 2, 2)
    return builder.as_markup()
