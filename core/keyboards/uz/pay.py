from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


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


def rkb_name_uz() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🔙 Orqaga')
    builder.button(text='🚪Asosiy menyu')

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def rkb_pay_uz() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='Click')
    builder.button(text='Paycom')
    builder.button(text='Kuryerga naqd pul')

    builder.button(text='🔙 Orqaga')
    builder.button(text='🚪Asosiy meny')

    builder.adjust(2, 1, 2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
