from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.database.db_users import Users
from core.keyboards.ru.reply import rkb_menu_ru
from core.keyboards.uz.reply import rkb_menu_uz
from core.utils.chat_cleaner import del_message, message_list

router = Router()


@router.message(F.text == "🚚 Yetkazib berish shartlari")
@router.message(F.text == "🚚 Условия доставки")
async def show_delivery(message: Message, bot: Bot, users: Users, state: FSMContext) -> None:
    await state.clear()

    await del_message(bot, message, message_list)

    language = await users.get_language(message.from_user.id)

    if language == 'ru':
        msg = await message.answer(
            text="""
            <b>Доставка</b>
Доставка осуществляется только по территории города Ташкент
Стоимость доставки в настоящий момент составляет 10 000 сум и оплачивается отдельно курьеру
Доставка осуществляется на следующий день после заказа в течение дня. 
Курьеры заранее звонят по оставленному Вам номеру и предупреждают об ориентировочном времени доставки
            """,
            parse_mode='HTML',
            reply_markup=rkb_menu_ru
        )
    else:
        msg = await message.answer(
            text="""
            <b>Yetkazib berish</b>
Yetkazib berish faqat Toshkent shahri hududida amalga oshiriladi
Hozirda yetkazib berish narxi 10 000 so'm va yetkazish xizmatiga alohida to'lanadi
Yetkazib berish kun davomida buyurtmadan keyingi kun amalga oshiriladi.
Yetkazuvchilar siz uchun qoldirilgan raqamga oldindan qo'ng'iroq qilishadi va taxminiy yetkazib berish muddati haqida ogohlantiradilar
            """,
            parse_mode='HTML',
            reply_markup=rkb_menu_uz
        )
    message_list.append(msg.message_id)
