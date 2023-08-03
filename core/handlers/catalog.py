from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.database.db_cart import Cart
from core.database.db_mysql import get_brands, get_lines, get_categories, get_products, get_product, get_category_id, \
    get_line_id, get_subcategories, get_subcategory_id
from core.database.db_users import Users
from core.keyboards.ru.catalog import rkb_brands, rkb_lines, rkb_categories, rkb_products, rkb_product, \
    rkb_product_in_cart, rkb_subcategories
from core.keyboards.uz.catalog import rkb_brands_uz, rkb_lines_uz, rkb_categories_uz, rkb_products_uz, rkb_product_uz, \
    rkb_product_in_cart_uz, rkb_subcategories_uz

from core.utils.chat_cleaner import del_message, message_list
from core.utils.states import UserState

router = Router()


@router.message(F.text == "🗂 Mahsulot katalogi")
@router.message(F.text == "🗂 Каталог продукции")
@router.message(F.text == "🔙 Назад")
@router.message(F.text == "🔙 Orqaga")
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
            reply_markup=rkb_brands(brands)
        )
    else:
        msg = await message.answer(
            text=f"""
            Brendni tanlang
            """,
            reply_markup=rkb_brands_uz(brands)
        )
    message_list.append(msg.message_id)

    await state.set_state(UserState.brand)


@router.message(F.text, UserState.brand)
@router.message(F.text == '🔙 Назад', UserState.lines)
@router.message(F.text == '🔙 Orqaga', UserState.lines)
async def show_lines(message: Message, bot: Bot, users: Users, state: FSMContext) -> None:
    brand_name = message.text
    await state.update_data(brand_name=brand_name)

    language = await users.get_language(message.from_user.id)
    brand_lines = await get_lines(brand_name)

    await del_message(bot, message, message_list)

    if language == 'ru':
        msg = await message.answer(
            text=f"""
            Выберите линейку продукции:
            """,
            reply_markup=rkb_lines(brand_lines)
        )
    else:
        msg = await message.answer(
            text=f"""
            Mahsulot qatorini tanlang:
            """,
            reply_markup=rkb_lines_uz(brand_lines)
        )
    message_list.append(msg.message_id)

    await state.set_state(UserState.lines)


@router.message(F.text, UserState.lines)
@router.message(F.text == '🔙 Назад', UserState.category)
@router.message(F.text == '🔙 Orqaga', UserState.category)
async def show_categories(message: Message, bot: Bot, users: Users, state: FSMContext) -> None:
    line_name = message.text.upper()
    line_id = await get_line_id(line_name)
    await state.update_data(line_name=line_name, line_id=line_id)

    language = await users.get_language(message.from_user.id)
    categories = await get_categories(language, line_name)

    await del_message(bot, message, message_list)

    if language == 'ru':
        msg = await message.answer(
            text=f"""
            Выберите категорию продукции:
            """,
            reply_markup=rkb_categories(categories, language)
        )
    else:
        msg = await message.answer(
            text=f"""
            Mahsulot toifasini tanlang:
            """,
            reply_markup=rkb_categories_uz(categories, language)
        )
    message_list.append(msg.message_id)

    await state.set_state(UserState.category)


@router.message(F.text, UserState.category)
@router.message(F.text == '🔙 Назад', UserState.product)
@router.message(F.text == '🔙 Orqaga', UserState.product)
async def show_subcategory(message: Message, bot: Bot, users: Users, state: FSMContext) -> None:
    category_name = message.text
    data = await state.get_data()
    line_id = data.get('line_id')
    category_id = await get_category_id(category_name, line_id)
    await state.update_data(category_name=category_name, category_id=category_id)

    language = await users.get_language(message.from_user.id)
    subcategories = await get_subcategories(language, category_id)

    await del_message(bot, message, message_list)

    if language == 'ru':
        msg = await message.answer(
            text=f"""
            Выберите категорию:
            """,
            reply_markup=rkb_subcategories(subcategories, language)
        )
    else:
        msg = await message.answer(
            text=f"""
            Kategoriyani tanlang:
            """,
            reply_markup=rkb_subcategories_uz(subcategories, language)
        )
    message_list.append(msg.message_id)

    await state.set_state(UserState.products)


@router.message(F.text, UserState.products)
@router.message(F.text == '🔙 Назад', UserState.product)
@router.message(F.text == '🔙 Orqaga', UserState.product)
async def show_products(message: Message, bot: Bot, users: Users, state: FSMContext) -> None:
    subcategory_name = message.text
    language = await users.get_language(message.from_user.id)
    subcategory_id = (await get_subcategory_id(subcategory_name, language))
    await state.update_data(subcategory_name=subcategory_name, subcategory_id=subcategory_id)

    products = await get_products(subcategory_id, language)

    await del_message(bot, message, message_list)

    if language == 'ru':
        msg = await message.answer(
            text=f"""
            Выберите продукт:
            """,
            reply_markup=rkb_products(products, language)
        )
    else:
        msg = await message.answer(
            text=f"""
            Mahsulotni tanlang:
            """,
            reply_markup=rkb_products_uz(products, language)
        )
    message_list.append(msg.message_id)

    await state.set_state(UserState.product)


@router.message(F.text, UserState.product)
@router.message(F.text == '🔙 Назад', UserState.cart)
@router.message(F.text == '🔙 Orqaga', UserState.cart)
async def show_product(message: Message, bot: Bot, users: Users, state: FSMContext) -> None:
    product_name = message.text
    await state.update_data(product_name=product_name)

    language = await users.get_language(message.from_user.id)

    await del_message(bot, message, message_list)

    product = await get_product(product_name, language)

    price = int(product['price'])

    product_title = product[f"title_{language}"].split(",")[:-1]
    title = ", ".join(product_title)
    photo = product['img'].split('.')[0]
    await state.update_data(title=title, photo=photo, price=price, product_id=product['id'])

    if language == 'ru':
        msg = await bot.send_photo(
            chat_id=message.from_user.id,
            photo=f"https://ecolavka.uz/public/media/{photo}.webp",
            caption=f"""
            {title}\n\nЦена - {price} сум
            """,
            reply_markup=rkb_product()
        )
    else:
        msg = await bot.send_photo(
            chat_id=message.from_user.id,
            photo=f"https://ecolavka.uz/public/media/{photo}.webp",
            caption=f"""
            {title}\n\nNarxi - {price} soʻm
            """,
            reply_markup=rkb_product_uz()
        )
    message_list.append(msg.message_id)

    await state.set_state(UserState.cart)


@router.message(F.text == '✅ Добавить в корзину', UserState.cart)
@router.message(F.text == "✅ Savatga qo'shish", UserState.cart)
async def add_product(message: Message, bot: Bot, cart: Cart, state: FSMContext) -> None:
    data = await state.get_data()
    product_id = data.get('product_id')
    language = data.get('language')
    title = data.get('title')
    photo = data.get('photo')
    price = data.get('price')

    await del_message(bot, message, message_list)

    await cart.add_to_cart(message.from_user.id, int(product_id), 1, int(price))

    if language == 'ru':
        msg = await bot.send_photo(
            chat_id=message.from_user.id,
            photo=f"https://ecolavka.uz/public/media/{photo}.webp",
            caption=f"""
            {title}\n\nЦена - {price} сум
            """,
            reply_markup=rkb_product_in_cart()
        )
    else:
        msg = await bot.send_photo(
            chat_id=message.from_user.id,
            photo=f"https://ecolavka.uz/public/media/{photo}.webp",
            caption=f"""
            {title}\n\nNarxi - {price} soʻm
            """,
            reply_markup=rkb_product_in_cart_uz()
        )
    message_list.append(msg.message_id)
