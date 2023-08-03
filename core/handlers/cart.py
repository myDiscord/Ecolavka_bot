from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.database.db_cart import Cart
from core.database.db_mysql import get_price
from core.database.db_users import Users
from core.keyboards.ru.cart import rkb_cart, rkb_cart_product
from core.keyboards.ru.reply import rkb_menu_ru
from core.keyboards.uz.cart import rkb_cart_uz, rkb_cart_product_uz
from core.keyboards.uz.reply import rkb_menu_uz
from core.utils.chat_cleaner import del_message, message_list
from core.utils.states import UserState

router = Router()


@router.message(F.text == "🧺 Savat")
@router.message(F.text == "🧺 Корзина")
@router.message(F.text == "🔙 Orqaga", UserState.in_cart)
@router.message(F.text == "🔙 Назад", UserState.in_cart)
async def show_cart(message: Message, bot: Bot, users: Users, cart: Cart, state: FSMContext) -> None:
    await state.clear()

    await del_message(bot, message, message_list)

    product_names = await cart.get_cart(message.from_user.id)
    language = await users.get_language(message.from_user.id)
    await state.update_data(language=language)

    if product_names:
        if language == 'ru':
            msg = await message.answer(
                text=f"""
                Ваша корзина:
                """,
                reply_markup=rkb_cart(product_names)
            )
        else:
            msg = await message.answer(
                text=f"""
                Savatingiz:
                """,
                reply_markup=rkb_cart_uz(product_names)
            )
            message_list.append(msg.message_id)

    else:
        if language == 'ru':
            msg = await message.answer(
                text=f"""
                Ваша корзина пуста
                """,
                reply_markup=rkb_menu_ru
            )
        else:
            msg = await message.answer(
                text=f"""
                Savatingiz bo'sh
                """,
                reply_markup=rkb_menu_uz
            )
    message_list.append(msg.message_id)

    await state.set_state(UserState.in_cart)


@router.message(F.text, UserState.in_cart)
async def show_product(message: Message, bot: Bot, users: Users, cart: Cart, state: FSMContext) -> None:
    product_name = message.text
    await state.update_data(product_name=product_name)

    language = await users.get_language(message.from_user.id)
    product_id, number = await cart.get_id_number(message.from_user.id, product_name)
    price = await get_price(product_id)

    if number == 1:
        text = ''
    else:
        if language == 'ru':
            text = f'- {number} шт'
        else:
            text = f'- {number} dona'
        price = price * number

    await del_message(bot, message, message_list)

    if language == 'ru':
        msg = await message.answer(
            text=f"""
                {product_name}
    
Цена - {price} {text}
            """,
            reply_markup=rkb_cart_product(number)
        )
    else:
        msg = await message.answer(
            text=f"""
            {product_name}

Narxi - {price} {text}
            """,
            reply_markup=rkb_cart_product_uz(number)
        )
    message_list.append(msg.message_id)


@router.message(F.text == '➕️больше', UserState.in_cart)
@router.message(F.text == "➕ko'proq", UserState.in_cart)
@router.message(F.text == '➖️меньше', UserState.in_cart)
@router.message(F.text == '➖kamroq', UserState.in_cart)
async def show_product(message: Message, bot: Bot, users: Users, cart: Cart, state: FSMContext) -> None:
    data = await state.get_data()
    product_name = data.get('product_name')

    language = await users.get_language(message.from_user.id)
    product_id, number = await cart.get_id_number(message.from_user.id, product_name)

    if message.text in ['➕️больше', "➕ko'proq"]:
        number += 1
    elif message.text in ['➖️меньше', '➖kamroq'] and number >= 2:
        number -= 1

    await cart.update_number(message.from_user.id, product_id, number)
    price = await get_price(product_id)

    if number == 1:
        text = ''
    else:
        if language == 'ru':
            text = f'- {number} шт'
        else:
            text = f'- {number} dona'
        price = price * number

    await del_message(bot, message, message_list)

    if language == 'ru':
        msg = await message.answer(
            text=f"""
                {product_name}

Цена - {price} {text}
            """,
            reply_markup=rkb_cart_product(number)
        )
    else:
        msg = await message.answer(
            text=f"""
            {product_name}

Narxi - {price} {text}
            """,
            reply_markup=rkb_cart_product_uz(number)
        )
    message_list.append(msg.message_id)


@router.message(F.text == '✖️удалить товар', UserState.in_cart)
@router.message(F.text == "✖️mahsulotni o'chirish", UserState.in_cart)
async def add_product(message: Message, users: Users, cart: Cart, state: FSMContext) -> None:
    data = await state.get_data()
    product_name = data.get('product_name')
    language = await users.get_language(message.from_user.id)

    await cart.delete_items(message.from_user.id, product_name)

    product_names = await cart.get_cart(message.from_user.id)

    if product_names:
        if language == 'ru':
            msg = await message.answer(
                text=f"""
                Товар удален из корзины\nВаша корзина:
                """,
                reply_markup=rkb_cart(product_names)
            )
        else:
            msg = await message.answer(
                text=f"""
                Buyum savatdan olib tashlandi\nSavatingiz:
                """,
                reply_markup=rkb_cart_uz(product_names)
            )
        message_list.append(msg.message_id)

    else:
        if language == 'ru':
            msg = await message.answer(
                text=f"""
                Ваша корзина пуста
                """,
                reply_markup=rkb_menu_ru
            )
        else:
            msg = await message.answer(
                text=f"""
                Savatingiz bo'sh
                """,
                reply_markup=rkb_menu_uz
            )
        message_list.append(msg.message_id)
