from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.database.db_cart import Cart
from core.database.db_mysql import get_brands, get_lines, get_categories, get_products, get_product
from core.database.db_users import Users
from core.keyboards.ru.catalog import ikb_brands, ikb_lines, ikb_categories, ikb_products, ikb_product, \
    ikb_product_in_cart
from core.keyboards.uz.catalog import ikb_brands_uz, ikb_lines_uz, ikb_categories_uz, ikb_products_uz, ikb_product_uz, \
    ikb_product_in_cart_uz

from core.utils.chat_cleaner import del_message, message_list, del_callback

router = Router()


@router.message(F.text == "🗂 Mahsulot katalogi")
@router.message(F.text == "🗂 Каталог продукции")
async def show_brands(message: Message, bot: Bot, users: Users, state: FSMContext) -> None:
    await state.clear()

    await del_message(bot, message, message_list)

    language = await users.get_language(message.from_user.id)

    brands = await get_brands()

    if language == 'ru':
        msg = await message.answer(
            text=f"""
            Выберите бренд
            """,
            reply_markup=ikb_brands(brands)
        )
    else:
        msg = await message.answer(
            text=f"""
            Brendni tanlang
            """,
            reply_markup=ikb_brands_uz(brands)
        )
    message_list.append(msg.message_id)


@router.callback_query(F.data == "Mahsulot katalogi")
@router.callback_query(F.data == "Каталог продукции")
async def show_brands(callback: CallbackQuery, users: Users) -> None:
    brands = await get_brands()

    language = await users.get_language(callback.from_user.id)

    if language == 'ru':
        msg = await callback.message.edit_text(
            text=f"""
            Выберите бренд
            """,
            reply_markup=ikb_brands(brands)
        )
    else:
        msg = await callback.message.edit_text(
            text=f"""
            Brendni tanlang
            """,
            reply_markup=ikb_brands_uz(brands)
        )
    message_list.append(msg.message_id)


@router.callback_query(F.data.startswith('ru_brand_'))
async def show_lines(callback: CallbackQuery, users: Users, state: FSMContext) -> None:
    brand_id = int(callback.data.split('_')[-1])

    language = await users.get_language(callback.from_user.id)

    await state.update_data(brand_id=brand_id)

    brand_lines = await get_lines(brand_id)

    if language == 'ru':
        msg = await callback.message.edit_text(
            text=f"""
            Выберите линейку продукции:
            """,
            reply_markup=ikb_lines(brand_lines)
        )
    else:
        msg = await callback.message.edit_text(
            text=f"""
            Mahsulot qatorini tanlang:
            """,
            reply_markup=ikb_lines_uz(brand_lines)
        )
    message_list.append(msg.message_id)


@router.callback_query(F.data.startswith('ru_brand-lines_'))
async def show_categories(callback: CallbackQuery, users: Users, state: FSMContext) -> None:
    line_id = callback.data.split('_')[-1]
    line_name = callback.data.split('_')[-2].split(' ')[-1].upper()

    data = await state.get_data()
    brand_id = data.get('brand_id')

    language = await users.get_language(callback.from_user.id)

    await state.update_data(line_name=line_name, line_id=line_id, language=language)

    categories = await get_categories(language, line_name)

    if language == 'ru':
        msg = await callback.message.edit_text(
            text=f"""
            Выберите категорию продукции:
            """,
            reply_markup=ikb_categories(categories, language, brand_id)
        )
    else:
        msg = await callback.message.edit_text(
            text=f"""
            Mahsulot toifasini tanlang:
            """,
            reply_markup=ikb_categories_uz(categories, language, brand_id)
        )
    message_list.append(msg.message_id)


@router.callback_query(F.data.startswith('category_'))
async def show_products(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    category_id = callback.data.split('_')[-1]

    await state.update_data(category_id=category_id)
    data = await state.get_data()
    line_name = data.get('line_name')
    line_id = data.get('line_id')
    language = data.get('language')

    products = await get_products(category_id, language)

    await del_callback(bot, callback, message_list)

    if language == 'ru':
        msg = await callback.message.answer(
            text=f"""
            Выберите продукт:
            """,
            reply_markup=ikb_products(products, language, line_id, line_name)
        )
    else:
        msg = await callback.message.answer(
            text=f"""
            Mahsulotni tanlang:
            """,
            reply_markup=ikb_products_uz(products, language, line_id, line_name)
        )
    message_list.append(msg.message_id)


@router.callback_query(F.data.startswith('product_'))
async def show_product(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    product_id = int(callback.data.split('_')[-1])
    number = int(callback.data.split('_')[-2])
    await state.update_data(product_id=product_id)
    data = await state.get_data()
    category_id = data.get('category_id')
    language = data.get('language')

    await del_callback(bot, callback, message_list)

    product = await get_product(product_id, language)

    if number == 1:
        text = ''
        price = int(product['price'])
    else:
        if language == 'ru':
            text = f'- {number} шт'
        else:
            text = f'- {number} dona'
        price = int(product['price']) * number

    product_title = product[f"title_{language}"].split(",")[:-1]
    title = ", ".join(product_title)
    photo = product['img'].split('.')[0]

    if language == 'ru':
        msg = await bot.send_photo(
            chat_id=callback.from_user.id,
            photo=f"https://ecolavka.uz/public/media/{photo}.webp",
            caption=f"""
            {title}\n\nЦена - {price} {text}
            """,
            reply_markup=ikb_product(product_id, number, category_id)
        )
    else:
        msg = await bot.send_photo(
            chat_id=callback.from_user.id,
            photo=f"https://ecolavka.uz/public/media/{photo}.webp",
            caption=f"""
            {title}\n\nNarxi - {price} {text}
            """,
            reply_markup=ikb_product_uz(product_id, number, category_id)
        )
    message_list.append(msg.message_id)


@router.callback_query(F.data.startswith('product_'))
async def show_product(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    product_id = int(callback.data.split('_')[-1])
    number = int(callback.data.split('_')[-2])
    await state.update_data(product_id=product_id)
    data = await state.get_data()
    category_id = data.get('category_id')
    language = data.get('language')

    await del_callback(bot, callback, message_list)

    product = await get_product(product_id, language)

    if number == 1:
        text = ''
        price = int(product['price'])
    else:
        if language == 'ru':
            text = f'- {number} шт'
        else:
            text = f'- {number} dona'
        price = int(product['price']) * number

    product_title = product[f"title_{language}"].split(",")[:-1]
    title = ", ".join(product_title)
    photo = product['img'].split('.')[0]

    if language == 'ru':
        msg = await bot.send_photo(
            chat_id=callback.from_user.id,
            photo=f"https://ecolavka.uz/public/media/{photo}.webp",
            caption=f"""
            {title}\n\nЦена - {price} {text}
            """,
            reply_markup=ikb_product(product_id, number, category_id)
        )
    else:
        msg = await bot.send_photo(
            chat_id=callback.from_user.id,
            photo=f"https://ecolavka.uz/public/media/{photo}.webp",
            caption=f"""
            {title}\n\nNarxi - {price} {text}
            """,
            reply_markup=ikb_product_uz(product_id, number, category_id)
        )
    message_list.append(msg.message_id)


@router.callback_query(F.data.startswith('cart-add_'))
async def add_product(callback: CallbackQuery, bot: Bot, cart: Cart, state: FSMContext) -> None:
    product_id = int(callback.data.split('_')[-1])
    number = int(callback.data.split('_')[-2])
    data = await state.get_data()
    category_id = data.get('category_id')
    language = data.get('language')

    await del_callback(bot, callback, message_list)

    if language == 'ru':
        await callback.answer('Товар добавлен в корзину')
    else:
        await callback.answer("Mahsulot savatga qo'shildi")

    await state.update_data(product_id=product_id)

    product = await get_product(product_id, language)

    await cart.add_to_cart(callback.from_user.id, product_id, number, int(product['price']))

    if number == 1:
        text = ''
        price = int(product['price'])
    else:
        if language == 'ru':
            text = f'- {number} шт'
        else:
            text = f'- {number} dona'
        price = int(product['price']) * number

    product_title = product[f"title_{language}"].split(",")[:-1]
    title = ", ".join(product_title)
    photo = product['img'].split('.')[0]

    if language == 'ru':
        msg = await bot.send_photo(
            chat_id=callback.from_user.id,
            photo=f"https://ecolavka.uz/public/media/{photo}.webp",
            caption=f"""
            {title}\n\nЦена - {price} {text}
            """,
            reply_markup=ikb_product_in_cart(category_id)
        )
    else:
        msg = await bot.send_photo(
            chat_id=callback.from_user.id,
            photo=f"https://ecolavka.uz/public/media/{photo}.webp",
            caption=f"""
            {title}\n\nNarxi - {price} {text}
            """,
            reply_markup=ikb_product_in_cart_uz(category_id)
        )
    message_list.append(msg.message_id)
