from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.database.db_users import Users
from core.keyboards.ru.reply import rkb_menu_ru
from core.keyboards.uz.reply import rkb_menu_uz
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
            
📱<a href="t.me/{settings.contacts.manager}">Связь с менеджером</a>
            """,
            parse_mode='HTML',
            reply_markup=rkb_menu_ru
        )
    else:
        msg = await message.answer(
            text=f"""
            ☎️ Aloqa telefon raqami: <code>{settings.contacts.phone}</code>
            
📱<a href="t.me/{settings.contacts.manager}">Chat menejeri</a>
            """,
            parse_mode='HTML',
            reply_markup=rkb_menu_uz
        )
    message_list.append(msg.message_id)
