from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from core.settings import settings


rkb_menu_uz = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text="🗂 Mahsulot katalogi"
        )
    ],
    [
        KeyboardButton(
            text="🚚 Yetkazib berish shartlari"
        ),
        KeyboardButton(
            text="☎️ Biz bilan bog'laning"
        )
    ],
    [
        KeyboardButton(
            text="📰 Yangiliklar"
        ),
        KeyboardButton(
            text="💼 Shaxsiy hisob"
        )
    ],
    [
        KeyboardButton(
            text="🧺 Savat"
        )
    ]
], resize_keyboard=True, one_time_keyboard=True, selective=True)


rkb_manager_uz = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text="💬 Online-чат",
            url=settings.contacts.manager
        ),
        KeyboardButton(
            text="🔙 Asosiy menyu"
        )
    ]
], resize_keyboard=True, one_time_keyboard=True, selective=True)


rkb_phone_uz = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text="📲 Telefon raqamini ulashing",
            request_contact=True
        )
    ],
    [
        KeyboardButton(
            text="🔙 Orqaga"
        ),
        KeyboardButton(
            text="🚪Asosiy menyu"
        )
    ]
], resize_keyboard=True, one_time_keyboard=True, selective=True)


rkb_geo_uz = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text="🗺 Joylashuvingizni yuboring",
            request_location=True
        )
    ],
    [
        KeyboardButton(
            text="🔙 Orqaga"
        ),
        KeyboardButton(
            text="🚪Asosiy menyu"
        )
    ]
], resize_keyboard=True, one_time_keyboard=True, selective=True)
