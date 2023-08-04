import json

from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, PreCheckoutQuery, LabeledPrice

from core.database.db_cart import Cart
from core.database.db_mysql import get_price, add_order, get_sd_id
from core.database.db_users import Users
from core.handlers.cart import show_cart
from core.keyboards.ru.pay import rkb_pay, rkb_name, rkb_phone, rkb_geo
from core.keyboards.ru.reply import rkb_menu_ru
from core.keyboards.uz.pay import rkb_pay_uz, rkb_name_uz, rkb_phone_uz, rkb_geo_uz
from core.keyboards.uz.reply import rkb_menu_uz
from core.settings import settings
from core.utils.chat_cleaner import message_list, del_message
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


@router.message(F.text == "🔙 Orqaga", UserState.name)
@router.message(F.text == "🔙 Назад", UserState.name)
async def back_to_cart(message: Message, bot: Bot, users: Users, cart: Cart, state: FSMContext) -> None:
    await state.clear()
    await show_cart(message, bot, users, cart, state)


@router.message(F.text == '💳 Заказать')
@router.message(F.text == '💳 Buyurtma')
@router.message(F.text == "🔙 Orqaga", UserState.phone)
@router.message(F.text == "🔙 Назад", UserState.phone)
async def buy(message: Message, users: Users, cart: Cart, state: FSMContext) -> None:
    product_ids, numbers, prices = await cart.get_full_cart(message.from_user.id)
    language = await users.get_language(message.from_user.id)

    amount = 0
    for index, product_id in enumerate(product_ids):
        price = await get_price(product_id)
        amount += int(price['price']) * numbers[index]

    await state.update_data(amount=amount)

    if language == 'ru':
        msg = await message.answer(
            text=f"""
            Введите, пожалуйста, свое имя
            """,
            reply_markup=rkb_name()
        )
    else:
        msg = await message.answer(
            text=f"""
            Iltimos, ismingizni yuboring
            """,
            reply_markup=rkb_name_uz()
        )
    message_list.append(msg.message_id)
    await state.set_state(UserState.name)


@router.message(F.text, UserState.name)
@router.message(F.text == '🔙 Назад', UserState.geo)
@router.message(F.text == '🔙 Orqaga', UserState.geo)
async def get_name(message: Message, users: Users, state: FSMContext) -> None:
    name = message.text
    await state.update_data(name=name)

    language = await users.get_language(message.from_user.id)

    if language == 'ru':
        msg = await message.answer(
            text=f"""
            {name}, oтправьте свой номер телефона или введите номер вручную
            """,
            reply_markup=rkb_phone
        )
    else:
        msg = await message.answer(
            text=f"""
            {name}, telefon raqamingizni yuboring yoki raqamni qo'lda kiriting
            """,
            reply_markup=rkb_phone_uz
        )
    message_list.append(msg.message_id)
    await state.set_state(UserState.phone)


@router.message(F.text, UserState.phone)
@router.message(F.contact, UserState.phone)
@router.message(F.text == '🔙 Назад', UserState.payment)
@router.message(F.text == '🔙 Orqaga', UserState.payment)
async def get_phone(message: Message, users: Users, state: FSMContext) -> None:
    if message.contact is not None and message.contact.phone_number:
        phone = message.contact.phone_number
    else:
        phone = message.text
    await state.update_data(phone=phone)

    language = await users.get_language(message.from_user.id)

    if language == 'ru':
        msg = await message.answer(
            text=f"""
            Ваш телефон: {phone}
Отправьте свою геопозицию или выберите точку доставки на карте 📎
            """,
            reply_markup=rkb_geo
        )
    else:
        msg = await message.answer(
            text=f"""
            Telefoningiz: {phone}
Joylashuvingizni kiriting yoki xaritada yetkazib berish nuqtasini tanlang 📎
            """,
            reply_markup=rkb_geo_uz
        )
    message_list.append(msg.message_id)
    await state.set_state(UserState.geo)


@router.message(F.location, UserState.geo)
@router.message(F.text, UserState.geo)
async def get_geo(message: Message, users: Users, state: FSMContext) -> None:
    geo = message.location
    await state.update_data(latitude=geo.latitude, longitude=geo.longitude)

    language = await users.get_language(message.from_user.id)

    data = await state.get_data()
    name = data.get('name')
    phone = data.get('phone')

    if language == 'ru':
        msg = await message.answer(
            text="""
            Выберите метод оплаты
            """,
            reply_markup=rkb_pay()
        )
    else:
        msg = await message.answer(
            text="""
            Toʻlov usulingizni tanlang
            """,
            reply_markup=rkb_pay_uz()
        )
    message_list.append(msg.message_id)
    await users.update_user_data(message.from_user.id, name, phone)

    await state.set_state(UserState.payment)


@router.message(F.text == 'Click', UserState.payment)
async def click(message: Message, bot: Bot, users: Users, state: FSMContext):
    data = await state.get_data()
    await state.update_data(payment='1')

    amount = int(data.get('amount'))

    language = await users.get_language(message.from_user.id)

    if language == 'ru':
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

    else:
        msg = await bot.send_invoice(
            chat_id=message.from_user.id,
            title='Xarid qilish',
            description=f'{amount} s\'om',
            payload='Payment through a core',
            provider_token=settings.wallet.click,
            currency='uzs',
            prices=[
                LabeledPrice(
                    label=f'Tovarlarni sotib olish {amount} s\'om',
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


@router.message(F.text == 'Paycom', UserState.payment)
async def pay_com(message: Message, bot: Bot, users: Users, state: FSMContext):
    data = await state.get_data()
    await state.update_data(payment='2')

    amount = int(data.get('amount'))

    language = await users.get_language(message.from_user.id)

    if language == 'ru':
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
    else:
        msg = await bot.send_invoice(
            chat_id=message.from_user.id,
            title='Xarid qilish',
            description=f'{amount} s\'om',
            payload='Payment through a core',
            provider_token=settings.wallet.pay_com,
            currency='uzs',
            prices=[
                LabeledPrice(
                    label=f'Tovarlarni sotib olish {amount} s\'om',
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

    await state.clear()
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

    language = await users.get_language(message.from_user.id)

    if language == 'ru':
        await message.answer(
            text=f"""
            Заказ сформирован, ожидайте доставку
            """,
            reply_markup=rkb_menu_ru
        )
    else:
        await message.answer(
            text=f"""
            Buyurtmangiz joylashtirildi, yetkazib berishni kuting.
            """,
            reply_markup=rkb_menu_uz
        )


@router.message(F.text == 'Наличными курьеру', UserState.payment)
@router.message(F.text == 'Kuryerga naqd pul', UserState.payment)
async def cash(message: Message, bot: Bot, users: Users, cart: Cart, state: FSMContext) -> None:
    data = await state.get_data()
    name = data.get('name')
    phone = data.get('phone')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    total = data.get('amount')
    payment_method = 3

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
                    products, total, '1', message.from_user.id)

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
Способ оплаты: Наличными при получении
К оплате: {total}
        """,
        parse_mode='HTML'
    )

    await cart.clear_cart(message.from_user.id)

    language = await users.get_language(message.from_user.id)

    if language == 'ru':
        await message.answer(
            text="""
            Заказ сформирован, ожидайте доставку
            """,
            reply_markup=rkb_menu_ru
        )
    else:
        await message.answer(
            text=f"""
            Buyurtmangiz joylashtirildi, yetkazib berishni kuting.
            """,
            reply_markup=rkb_menu_uz
        )

    await state.clear()
