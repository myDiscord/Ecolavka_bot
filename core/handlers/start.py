from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.database.db_users import Users
from core.keyboards.ru.reply import rkb_language, rkb_menu_ru
from core.keyboards.uz.reply import rkb_menu_uz
from core.utils.chat_cleaner import message_list, del_callback

router = Router()


@router.message(F.text == '🚪Asosiy menyu')
@router.message(F.text == '🚪Главное меню')
@router.message(Command(commands='start'))
async def cmd_start(message: Message, users: Users, state: FSMContext) -> None:
    await state.clear()

    language = await users.get_language(message.from_user.id)

    if not language:
        msg = await message.answer(
            text="""
            Tilni tanlang | Выберите язык 
            """,
            reply_markup=rkb_language
        )
    elif language == 'ru':
        msg = await message.answer(
            text="""
            Добро пожаловать в MAYERI – ЭКО лавку!
            """,
            reply_markup=rkb_menu_ru
        )
    else:
        msg = await message.answer(
            text="""
            MAYERI - ECO do'koniga xush kelibsiz!
            """,
            reply_markup=rkb_menu_uz
        )
    message_list.append(msg.message_id)
