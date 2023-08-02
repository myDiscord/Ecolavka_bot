import re

from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery

from core.database.db_mysql import get_news, get_post
from core.database.db_users import Users
from core.keyboards.ru.news import ikb_news, ikb_post
from core.keyboards.uz.news import ikb_news_uz, ikb_post_uz
from core.utils.chat_cleaner import del_message, del_callback, message_list

router = Router()


@router.message(F.text == "📰 Yangiliklar")
@router.message(F.text == "📰 Новости")
async def show_news(message: Message, bot: Bot, users: Users) -> None:
    await del_message(bot, message, message_list)

    language = await users.get_language(message.from_user.id)

    news = await get_news(language)

    if language == 'ru':
        msg = await message.answer(
            text=f"""
            Новости и акции:
            """,
            reply_markup=ikb_news(news, language)
        )
    else:
        msg = await message.answer(
            text=f"""
            Yangiliklar va aktsiyalar:
            """,
            reply_markup=ikb_news_uz(news, language)
        )
    message_list.append(msg.message_id)


@router.callback_query(F.data.startswith("news_"))
async def back_next(callback: CallbackQuery, bot: Bot, users: Users) -> None:
    current_page = int(callback.data.split('_')[-1])

    await del_callback(bot, callback, message_list)

    language = await users.get_language(callback.from_user.id)

    news = await get_news(language)

    if language == 'ru':
        msg = await callback.message.answer(
            text=f"""
            Новости и акции:
            """,
            reply_markup=ikb_news(news, language, current_page)
        )
    else:
        msg = await callback.message.answer(
            text=f"""
            Yangiliklar va aktsiyalar:
            """,
            reply_markup=ikb_news_uz(news, language, current_page)
        )
    message_list.append(msg.message_id)


@router.callback_query(F.data.startswith("post_"))
async def show_post(callback: CallbackQuery, bot: Bot, users: Users) -> None:
    post_id = int(callback.data.split('_')[-1])
    current_page = int(callback.data.split('_')[-2])

    await del_callback(bot, callback, message_list)

    language = await users.get_language(callback.from_user.id)

    post = await get_post(language, post_id)

    cleaned_text = re.sub(r'<.*?>', '', post[f'text_{language}'])

    photo = post['img'].split('.')[0]
    msg = await bot.send_photo(
        chat_id=callback.from_user.id,
        photo=f"https://ecolavka.uz/public/media/{photo}.webp"
    )
    message_list.append(msg.message_id)

    if language == 'ru':
        msg = await callback.message.answer(
            text=f"{post[f'title_{language}']}\n\n{cleaned_text}",
            parse_mode='HTML',
            reply_markup=ikb_post(current_page)
        )
    else:
        msg = await callback.message.answer(
            text=f"{post[f'title_{language}']}\n\n{cleaned_text}",
            parse_mode='HTML',
            reply_markup=ikb_post_uz(current_page)
        )
    message_list.append(msg.message_id)


@router.callback_query(F.data == "-")
async def error(callback: CallbackQuery) -> None:
    await callback.answer(
        text="""
        Перемотка недоступна
        """
    )


@router.callback_query(F.data == "+")
async def error(callback: CallbackQuery) -> None:
    await callback.answer(
        text="""
        Orqaga o'tkazish imkonsiz
        """
    )


@router.callback_query(F.data.startswith('list_ru_'))
async def get_list(callback: CallbackQuery) -> None:
    current = callback.data.split('_')[2]
    end = callback.data.split('_')[-1]

    await callback.answer(
        text=f"""
        Страница {current}/{end}
        """
    )


@router.callback_query(F.data.startswith('list_uz_'))
async def get_list(callback: CallbackQuery) -> None:
    current = callback.data.split('_')[2]
    end = callback.data.split('_')[-1]

    await callback.answer(
        text=f"""
        Sahifa {current}/{end}
        """
    )
