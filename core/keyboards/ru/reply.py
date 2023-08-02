from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from core.settings import settings

rkb_language = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text="🇺🇿 О'zbek"
        ),
        KeyboardButton(
            text="🇷🇺 Русский"
        )
    ]
], resize_keyboard=True, one_time_keyboard=True, selective=True)


rkb_menu_ru = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='🗂 Каталог продукции'
        )
    ],
    [
        KeyboardButton(
            text='🚚 Условия доставки'
        ),
        KeyboardButton(
            text='☎️ Связаться с нами'
        )
    ],
    [
        KeyboardButton(
            text='📰 Новости'
        ),
        KeyboardButton(
            text='💼 Личный кабинет'
        )
    ],
    [
        KeyboardButton(
            text='🧺 Корзина'
        )
    ]
], resize_keyboard=True, one_time_keyboard=True, selective=True)


rkb_manager = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text="💬 Online-чат",
            url=settings.contacts.manager
        ),
        KeyboardButton(
            text='🔙 Главное меню'
        )
    ]
], resize_keyboard=True, one_time_keyboard=True, selective=True)


rkb_phone = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text="📲 Поделиться номером телефона",
            request_contact=True
        )
    ],
    [
        KeyboardButton(
            text="🔙 Назад"
        ),
        KeyboardButton(
            text="🚪Главное меню"
        )
    ]
], resize_keyboard=True, one_time_keyboard=True, selective=True)


rkb_geo = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text="🗺 Отправить свою геопозицию",
            request_location=True
        )
    ],
    [
        KeyboardButton(
            text="🔙 Назад"
        ),
        KeyboardButton(
            text="🚪Главное меню"
        )
    ]
], resize_keyboard=True, one_time_keyboard=True, selective=True)
