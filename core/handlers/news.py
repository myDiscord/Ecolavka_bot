import re

from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.database.db_mysql import get_news, get_post
from core.database.db_users import Users
from core.keyboards.ru.news import rkb_news, rkb_post
from core.keyboards.uz.news import rkb_news_uz, rkb_post_uz
from core.utils.chat_cleaner import del_message, message_list
from core.utils.states import UserState

router = Router()


@router.message(F.text == "📰 Yangiliklar")
@router.message(F.text == "📰 Новости")
@router.message(F.text == "📰 Orqaga", UserState.news)
@router.message(F.text == "📰 Новости", UserState.news)
async def show_news(message: Message, bot: Bot, users: Users, state: FSMContext) -> None:
    await state.clear()

    await del_message(bot, message, message_list)

    language = await users.get_language(message.from_user.id)

    news = await get_news(language)

    if language == 'ru':
        msg = await message.answer(
            text=f"""
            Новости и акции:
            """,
            reply_markup=rkb_news(news, language)
        )
    else:
        msg = await message.answer(
            text=f"""
            Yangiliklar va aktsiyalar:
            """,
            reply_markup=rkb_news_uz(news, language)
        )
    message_list.append(msg.message_id)

    await state.set_state(UserState.news)


@router.message(F.text, UserState.news)
async def show_post(message: Message, bot: Bot, users: Users) -> None:
    post_id = int(message.text)

    await del_message(bot, message, message_list)

    language = await users.get_language(message.from_user.id)

    post = await get_post(language, post_id)

    cleaned_text = re.sub(r'<.*?>', '', post[f'text_{language}'])

    photo = post['img'].split('.')[0]
    msg = await bot.send_photo(
        chat_id=message.from_user.id,
        photo=f"https://ecolavka.uz/public/media/{photo}.webp"
    )
    message_list.append(msg.message_id)

    if language == 'ru':
        msg = await message.answer(
            text=f"{post[f'title_{language}']}\n\n{cleaned_text}",
            parse_mode='HTML',
            reply_markup=rkb_post()
        )
    else:
        msg = await message.answer(
            text=f"{post[f'title_{language}']}\n\n{cleaned_text}",
            parse_mode='HTML',
            reply_markup=rkb_post_uz()
        )
    message_list.append(msg.message_id)
