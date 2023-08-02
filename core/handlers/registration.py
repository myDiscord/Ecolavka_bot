from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.database.db_users import Users
from core.keyboards.ru.reply import rkb_menu_ru
from core.keyboards.uz.reply import rkb_menu_uz
from core.utils.chat_cleaner import del_message, message_list

router = Router()


@router.message(F.text == "🇷🇺 Русский")
async def get_language(message: Message, bot: Bot, users: Users, state: FSMContext) -> None:
    await state.update_data(language='ru')

    await del_message(bot, message, message_list)

    await users.add_user(message.from_user.id, 'ru')

    msg = await message.answer(
        text="""
        Добро пожаловать в MAYERI – ЭКО лавку!
        """,
        reply_markup=rkb_menu_ru
    )
    message_list.append(msg.message_id)


@router.message(F.text == "🇺🇿 О'zbek")
async def get_language(message: Message, bot: Bot, users: Users, state: FSMContext) -> None:
    await state.update_data(language='uz')

    await del_message(bot, message, message_list)

    await users.add_user(message.from_user.id, 'uz')

    msg = await message.answer(
        text="""
        MAYERI - ECO do'koniga xush kelibsiz!
        """,
        reply_markup=rkb_menu_uz
    )
    message_list.append(msg.message_id)
