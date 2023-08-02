import json

from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, LabeledPrice

from core.database.db_cart import Cart
from core.database.db_mysql import get_price, add_order, get_sd_id
from core.database.db_users import Users
from core.keyboards.ru.pay import ikb_pay, ikb_name
from core.keyboards.ru.reply import rkb_menu_ru, rkb_phone, rkb_geo
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


@router.callback_query(F.data == "pay_ru")
async def buy(callback: CallbackQuery, cart: Cart, state: FSMContext) -> None:
    product_ids, numbers = await cart.get_cart(callback.from_user.id)

    amount = 0
    for index, product_id in enumerate(product_ids):
        price = await get_price(product_id, 'ru')
        amount += int(price['price']) * numbers[index]

    await state.update_data(amount=amount)

    await callback.message.edit_text(
        text=f"""
        Введите, пожалуйста, свое имя
        """,
        reply_markup=ikb_name()
    )
    await state.set_state(UserState.name_ru)


@router.message(F.text == "🔙 Назад")
async def buy(message: Message, cart: Cart, state: FSMContext) -> None:
    product_ids, numbers = await cart.get_cart(message.from_user.id)

    amount = 0
    for index, product_id in enumerate(product_ids):
        price = await get_price(product_id, 'ru')
        amount += int(price['price']) * numbers[index]

    await state.update_data(amount=amount)

    msg = await message.edit_text(
        text=f"""
        Отправьте, пожалуйста, свое имя
        """,
        reply_markup=ikb_name()
    )
    await state.set_state(UserState.name_ru)
    message_list.append(msg.message_id)


@router.message(F.text, UserState.name_ru)
async def get_name(message: Message, state: FSMContext) -> None:
    name = message.text

    await state.update_data(name=name)

    # await del_message(bot, message, message_list)

    msg = await message.answer(
        text=f"""
        {name}, oтправьте свой номер телефона или введите номер вручную
        """,
        reply_markup=rkb_phone
    )
    message_list.append(msg.message_id)
    await state.set_state(UserState.phone_ru)


@router.message(F.contact, UserState.phone_ru)
async def get_phone(message: Message, state: FSMContext) -> None:
    phone = message.contact.phone_number

    await state.update_data(phone=phone)

    # await del_message(bot, message, message_list)

    msg = await message.answer(
        text=f"""
        Ваш телефон: {phone}
Отправьте свою геопозицию или выберите точку доставки на карте 📎
        """,
        reply_markup=rkb_geo
    )
    message_list.append(msg.message_id)
    await state.set_state(UserState.geo_ru)


@router.message(F.text, UserState.phone_ru)
async def get_phone(message: Message, state: FSMContext) -> None:
    phone = message.text

    await state.update_data(phone=phone)

    # await del_message(bot, message, message_list)

    msg = await message.answer(
        text=f"""
        Ваш телефон: {phone}
Отправьте свою геопозицию или выберите точку доставки на карте 📎
        """,
        reply_markup=rkb_geo
    )
    message_list.append(msg.message_id)
    await state.set_state(UserState.geo_ru)


@router.message(F.location, UserState.geo_ru)
@router.message(F.text, UserState.geo_ru)
async def get_geo(message: Message, users: Users, state: FSMContext) -> None:
    geo = message.location
    await state.update_data(latitude=geo.latitude, longitude=geo.longitude)

    data = await state.get_data()
    name = data.get('name')
    phone = data.get('phone')

    # await del_message(bot, message, message_list)

    msg = await message.answer(
        text="""
        Выберите метод оплаты
        """,
        reply_markup=ikb_pay()
    )
    message_list.append(msg.message_id)
    await users.update_user_data(message.from_user.id, name, phone)


@router.callback_query(F.data == 'CLICK')
async def click(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await state.update_data(payment='1')

    amount = int(data.get('amount'))

    msg = await bot.send_invoice(
        chat_id=message.from_user.id,
        title='Покупка товаров',
        description=f'{amount} сум.',
        payload='Payment through a core',
        provider_token=settings.wallet.click,
        currency='uzs',
        prices=[
            LabeledPrice(
                label=f'Покупка товаров на {amount} сум.',
                amount=amount * 100
            )
        ],
        start_parameter=f'{settings.wallet.start_parameter}',
        provider_data=None,
        photo_url=f'{settings.wallet.logo}',
        photo_size=100,
        photo_width=800,
        photo_height=450,
        need_name=False,
        need_phone_number=False,
        need_email=False,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=False,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=None,
        request_timeout=15
    )
    message_list.append(msg.message_id)


@router.callback_query(F.data == 'PAYCOM')
async def pay_com(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await state.update_data(payment='2')

    amount = int(data.get('amount'))

    msg = await bot.send_invoice(
        chat_id=message.from_user.id,
        title='Покупка товаров',
        description=f'{amount} сум.',
        payload='Payment through a core',
        provider_token=settings.wallet.pay_com,
        currency='uzs',
        prices=[
            LabeledPrice(
                label=f'Покупка товаров на {amount} сум.',
                amount=amount * 100
            )
        ],
        start_parameter=f'{settings.wallet.start_parameter}',
        provider_data=None,
        photo_url=f'{settings.wallet.logo}',
        photo_size=100,
        photo_width=800,
        photo_height=450,
        need_name=False,
        need_phone_number=False,
        need_email=False,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=False,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=None,
        request_timeout=15
    )
    message_list.append(msg.message_id)


@router.pre_checkout_query()
async def confirm(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.successful_payment)
async def payment(message: Message, bot, users: Users, cart: Cart, state: FSMContext):
    data = await state.get_data()
    name = data.get('name')
    phone = data.get('phone')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    total = data.get('amount')
    payment_method = data.get('payment')

    await del_message(bot, message, message_list)

    city, address = get_location_info(latitude, longitude)

    product_ids, numbers, prices = await cart.get_full_cart(message.from_user.id)
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
                    products, total, '2', message.from_user.id)

    if payment_method == '1':
        text = 'click'
    else:
        text = 'paycom'

    client_id = await users.get_client_id(message.from_user.id)
    if not client_id:
        client_id = await create_client(name, phone, address)
        await users.add_client_id(message.from_user.id, client_id)

    products_crm = await to_crm(message.from_user.id, cart)
    await create_order(client_id, total, products_crm)

    await bot.send_message(
        chat_id=settings.contacts.group,
        text=f"""
        Форма: Заказ в боте
Имя: {name}
Телефон: <code>{phone}</code>
Способ оплаты: {text}
К оплате: {total}
        """,
        parse_mode='HTML'
    )

    await cart.clear_cart(message.from_user.id)

    await message.answer(
        text=f"""
        Заказ сформирован, ожидайте доставку
        """,
        reply_markup=rkb_menu_ru
    )


@router.callback_query(F.data == "CASH")
async def cash(callback: CallbackQuery, bot: Bot, users: Users, cart: Cart, state: FSMContext) -> None:
    data = await state.get_data()
    name = data.get('name')
    phone = data.get('phone')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    total = data.get('amount')
    payment_method = 3

    await del_callback(bot, callback, message_list)

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
        Заказ сформирован, ожидайте доставку
        """,
        reply_markup=rkb_menu_ru
    )
