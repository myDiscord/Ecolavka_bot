from bs4 import BeautifulSoup

from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.database.db_mysql import get_history, get_name, get_history_order
from core.database.db_users import Users
from core.keyboards.ru.account import rkb_account, rkb_account_2
from core.keyboards.ru.reply import rkb_menu_ru
from core.keyboards.uz.account import rkb_account_uz, rkb_account_2_uz
from core.keyboards.uz.reply import rkb_menu_uz
from core.utils.chat_cleaner import del_message, message_list
from core.utils.states import UserState

router = Router()


async def get_data(data):
    updated_at = data['updated_at']

    soup = BeautifulSoup(data['products'], 'html.parser')
    products = []
    for cart_item in soup.find_all('div', class_='cart-item'):
        product_id = cart_item.find('h4', class_='cart-item-title').text.strip()

        product_id = product_id.split(',', 1)[0]

        quantity = cart_item.find('div', class_='cart-col').next_sibling.strip()
        price = cart_item.find_all('div', class_='cart-col')[-1].text.strip()
        products.append({
            'id': product_id,
            'quantity': quantity,
            'price': price
        })

    return updated_at, products


async def create_product_text(products, language):
    text = ''
    for product in products:
        if product['id'].isdigit():
            product['id'] = await get_name(product, language)
        product_text = f"{product['id']} - {product['quantity']} шт - {product['price']=}"
        text += product_text + '\n'
    return text


@router.message(F.text == "💼 Shaxsiy hisob")
@router.message(F.text == "💼 Личный кабинет")
@router.message(F.text == "🔙 Назад", UserState.account)
@router.message(F.text == "🔙 Orqaga", UserState.account)
async def show_account(message: Message, bot: Bot, users: Users, state: FSMContext) -> None:
    await state.clear()

    await del_message(bot, message, message_list)

    language = await users.get_language(message.from_user.id)
    phone = await users.get_phone(message.from_user.id)

    data = await get_history(phone, message.from_user.id)
    if data is None:
        if language == 'ru':
            msg = await message.answer(
                text="""
                Вы еще не совершили ни одного заказа.
                """,
                reply_markup=rkb_menu_ru
            )
        else:
            msg = await message.answer(
                text="""
                Siz hali hech qanday buyurtma bermadingiz.
                """,
                reply_markup=rkb_menu_uz
            )
        message_list.append(msg.message_id)

    else:
        if language == 'ru':
            msg = await message.answer(
                text="""
                Ваши заказы:
                """,
                reply_markup=rkb_account(data)
            )
        else:
            msg = await message.answer(
                text="""
                Sizning buyurtmalaringiz:
                """,
                reply_markup=rkb_account_uz(data)
            )
        message_list.append(msg.message_id)

    await state.set_state(UserState.account)


@router.message(F.text == "🇺🇿 Сменить язык", UserState.account)
@router.message(F.text == "🇷🇺 Tilni o'zgartirish", UserState.account)
async def change_language(message: Message, bot: Bot, users: Users) -> None:
    text = message.text

    await del_message(bot, message, message_list)

    if text == "🇺🇿 Сменить язык":
        await users.change_language(message.from_user.id, 'uz')

        msg = await message.answer(
            text="""
            Til o'zgartirildi
            """,
            reply_markup=rkb_menu_uz
        )

    else:
        await users.change_language(message.from_user.id, 'ru')

        msg = await message.answer(
            text="""
            Язык изменен
            """,
            reply_markup=rkb_menu_ru
        )
    message_list.append(msg.message_id)


@router.message(F.text, UserState.account)
async def order(message: Message, bot: Bot, users: Users) -> None:
    updated_at = message.text.split(': ')[-1]

    await del_message(bot, message, message_list)

    products_list = await get_history_order(updated_at)
    language = await users.get_language(message.from_user.id)

    for item in products_list:
        product = str(item['id'])
        if product.isdigit():
            new_product_info = await get_name(int(product), language)
            product_title = new_product_info[f"title_{language}"].split(",")[:-1]
            title = ", ".join(product_title)
            item['id'] = title

    new_products_str = "\n".join(
        [f"{item['id']} - {item['quantity']} шт, по {item['price']} за шт.\n" if language == 'ru' else
         f"{item['id']} - {item['quantity']} dona, {item['price']} dona uchun.\n" for item in
         products_list])

    if language == 'ru':
        msg = await message.answer(
            text=f"""
            {new_products_str}
            """,
            reply_markup=rkb_account_2()
        )
    else:
        msg = await message.answer(
            text=f"""
            {new_products_str}
            """,
            reply_markup=rkb_account_2_uz()
        )
    message_list.append(msg.message_id)
