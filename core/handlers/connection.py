from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.database.db_users import Users
from core.keyboards.ru.conection import ikb_connection
from core.keyboards.uz.conection import ikb_connection_uz
from core.settings import settings
from core.utils.chat_cleaner import del_message, message_list

router = Router()


@router.message(F.text == "☎️ Biz bilan bog'laning")
@router.message(F.text == "☎️ Связаться с нами")
async def show_connection(message: Message, bot: Bot, users: Users, state: FSMContext) -> None:
    await state.clear()

    await del_message(bot, message, message_list)

    language = await users.get_language(message.from_user.id)

    if language == 'ru':
        msg = await message.answer(
            text=f"""
            ☎️ Контактный телефон: <code>{settings.contacts.phone}</code>
            """,
            parse_mode='HTML',
            reply_markup=ikb_connection()
        )
    else:
        msg = await message.answer(
            text=f"""
            ☎️ Aloqa telefon raqami: <code>{settings.contacts.phone}</code>
            """,
            parse_mode='HTML',
            reply_markup=ikb_connection_uz()
        )
    message_list.append(msg.message_id)
