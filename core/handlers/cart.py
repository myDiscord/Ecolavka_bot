from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.database.db_cart import Cart
from core.database.db_mysql import get_product
from core.database.db_users import Users
from core.keyboards.ru.cart import ikb_cart, ikb_cart_product
from core.keyboards.ru.reply import rkb_menu_ru
from core.keyboards.uz.cart import ikb_cart_uz, ikb_cart_product_uz
from core.keyboards.uz.reply import rkb_menu_uz
from core.utils.chat_cleaner import del_message, message_list, del_callback

router = Router()


@router.message(F.text == "🧺 Savat")
@router.message(F.text == "🧺 Корзина")
async def show_cart(message: Message, bot: Bot, users: Users, cart: Cart, state: FSMContext) -> None:
    await state.clear()

    await del_message(bot, message, message_list)

    product_ids, numbers = await cart.get_cart(message.from_user.id)
    language = await users.get_language(message.from_user.id)
    await state.update_data(language=language)

    products = []
    if product_ids is not None:
        for product_id in product_ids:
            products.append(await get_product(product_id, language))

        if language == 'ru':
            msg = await message.answer(
                text=f"""
                Ваша корзина:
                """,
                reply_markup=ikb_cart(products, numbers, language)
            )
        else:
            msg = await message.answer(
                text=f"""
                Savatingiz:
                """,
                reply_markup=ikb_cart_uz(products, numbers, language)
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


@router.callback_query(F.data == "cart_ru")
async def show_cart(callback: CallbackQuery, bot: Bot, users: Users, cart: Cart) -> None:
    product_ids, numbers = await cart.get_cart(callback.from_user.id)
    language = await users.get_language(callback.from_user.id)

    await del_callback(bot, callback, message_list)

    products = []
    if product_ids is not None:
        for product_id in product_ids:
            products.append(await get_product(product_id, language))

        if language == 'ru':
            msg = await callback.message.answer(
                text=f"""
                Ваша корзина:
                """,
                reply_markup=ikb_cart(products, numbers, language)
            )
        else:
            msg = await callback.message.answer(
                text=f"""
                Savatingiz:
                """,
                reply_markup=ikb_cart_uz(products, numbers, language)
            )
            message_list.append(msg.message_id)

    else:
        if language == 'ru':
            msg = await callback.message.answer(
                text=f"""
                Ваша корзина пуста
                """,
                reply_markup=rkb_menu_ru
            )
        else:
            msg = await callback.message.answer(
                text=f"""
                Savatingiz bo'sh
                """,
                reply_markup=rkb_menu_uz
            )
    message_list.append(msg.message_id)


@router.callback_query(F.data.startswith('cart_'))
async def show_product(callback: CallbackQuery, bot: Bot, cart: Cart, state: FSMContext) -> None:
    product_id = int(callback.data.split('_')[-1])
    number = int(callback.data.split('_')[-2])
    data = await state.get_data()
    language = data.get('language')

    product = await get_product(product_id, language)

    await cart.update_number(callback.from_user.id, product_id, number)

    await del_callback(bot, callback, message_list)

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

    if language == 'ru':
        msg = await callback.message.answer(
            text=f"""
                {title}
    
Цена - {price} {text}
            """,
            reply_markup=ikb_cart_product(product_id, number)
        )
    else:
        msg = await callback.message.answer(
            text=f"""
            {title}

Narxi - {price} {text}
            """,
            reply_markup=ikb_cart_product_uz(product_id, number)
        )
    message_list.append(msg.message_id)


@router.callback_query(F.data.startswith('cart-del_'))
async def add_product(callback: CallbackQuery, cart: Cart, state: FSMContext) -> None:
    product_id = int(callback.data.split('_')[-1])
    data = await state.get_data()
    language = data.get('language')

    await cart.delete_items(callback.from_user.id, product_id)

    if language == 'ru':
        await callback.answer('Товар удален из корзины')
    else:
        await callback.answer('Buyum savatdan olib tashlandi')

    product_ids, numbers = await cart.get_cart(callback.from_user.id)

    products = []
    if product_ids is not None:
        for product_id in product_ids:
            products.append(await get_product(product_id, language))

            if language == 'ru':
                msg = await callback.message.answer(
                    text=f"""
                    Ваша корзина:
                    """,
                    reply_markup=ikb_cart(products, numbers, language)
                )
            else:
                msg = await callback.message.answer(
                    text=f"""
                    Savatingiz:
                    """,
                    reply_markup=ikb_cart_uz(products, numbers, language)
                )
            message_list.append(msg.message_id)

    else:
        if language == 'ru':
            msg = await callback.message.answer(
                text=f"""
                Ваша корзина пуста
                """,
                reply_markup=rkb_menu_ru
            )
        else:
            msg = await callback.message.answer(
                text=f"""
                Savatingiz bo'sh
                """,
                reply_markup=rkb_menu_uz
            )
        message_list.append(msg.message_id)
