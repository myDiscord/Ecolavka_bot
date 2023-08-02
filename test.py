import json

from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, LabeledPrice

from core.database.db_cart import Cart
from core.database.db_mysql import get_price, add_order, get_sd_id
from core.database.db_users import Users
from core.keyboards.uz.pay import ikb_pay_uz, ikb_name_uz
from core.keyboards.uz.reply import rkb_menu_uz, rkb_phone_uz, rkb_geo_uz
from core.settings import settings
from core.utils.chat_cleaner import message_list, del_message, del_callback
from core.utils.crm import create_client, create_order
from core.utils.location_info import get_location_info
from core.utils.states import UserState

router = Router()


async def to_crm(callback_user_id, cart: Cart):
    product_ids, numbers, prices = await cart.get_full_cart(callback_user_id)

    products_list = []
    for product_id, quantity, price in zip(product_ids, numbers, prices):
        sd_id = await get_sd_id(product_id)
        product_data = {
            "product": {
                "SD_id": sd_id,
            },
            "quantity": quantity,
            "price": price,
        }
        products_list.append(product_data)

    return products_list


@router.message(F.text == "1")
async def cash(message: Message, bot: Bot, users: Users, cart: Cart, state: FSMContext) -> None:
    data = await state.get_data()
    name = 'name'
    phone = '0123456789'
    latitude = '11.1'
    longitude = '11.1'
    total = 100
    payment_method = 3

    await del_callback(bot, message, message_list)

    city, address = get_location_info(latitude, longitude)

    product_ids, numbers, prices = await cart.get_full_cart(callback.from_user.id)
    products_list = [
        {
            "id": str(product_id),
            "quantity": str(quantity),
            "price": str(price),
        }
        for product_id, quantity, price in zip(product_ids, numbers, prices)
    ]

    products = json.dumps(products_list, indent=2)
    await add_order(name, phone, city, address, payment_method,
                    products, total, '1', callback.from_user.id)

    client_id = await users.get_client_id(callback.from_user.id)
    if not client_id:
        client_id = await create_client(name, phone, address)
        await users.add_client_id(callback.from_user.id, client_id)

    products_crm = await to_crm(callback.from_user.id, cart)
    print(products_crm)
    await create_order(client_id, total, products_crm)

    await bot.send_message(
        chat_id=settings.contacts.group,
        text=f"""
        Форма: Заказ в боте
Имя: {name}
Телефон: <code>{phone}</code>
Способ оплаты: Наличными при получении
К оплате: {total}
        """,
        parse_mode='HTML'
    )

    await cart.clear_cart(callback.from_user.id)

    await callback.message.answer(
        text="""
        Buyurtmangiz joylashtirildi, yetkazib berishni kuting.
        """,
        reply_markup=rkb_menu_uz
    )
