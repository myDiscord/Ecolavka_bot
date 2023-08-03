from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


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


def rkb_name() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🔙 Назад')
    builder.button(text='🚪Главное меню')

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def rkb_pay() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='Click')
    builder.button(text='Paycom')
    builder.button(text='Наличными курьеру')

    builder.button(text='🔙 Назад')
    builder.button(text='🚪Главное меню')

    builder.adjust(2, 1, 2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
