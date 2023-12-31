import asyncpg
import asyncio
import logging
import contextlib

from aiogram import Bot, Dispatcher

from core.database.db_cart import Cart
from aiogram.fsm.storage.redis import RedisStorage

from core.database.db_users import Users

from core.settings import settings

from core.utils.commands import set_commands
from core.utils.db_create import check_database_exists, create_database

from core.handlers.routers import user_router


async def start_bot(bot: Bot, users: Users, cart: Cart) -> None:
    await set_commands(bot)
    await users.create_users_table_if_not_exists()
    await cart.create_cart_table_if_not_exists()


async def stop_bot() -> None:
    pass


async def create_pool():
    return await asyncpg.create_pool(
        user=settings.db.db_user, password=settings.db.db_password, database=settings.db.db_database,
        host=settings.db.db_host, port=settings.db.db_port, command_timeout=60
    )


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )

    database_exists = await check_database_exists()
    if not database_exists:
        await create_database()

    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    pool_connect = await create_pool()
    storage = RedisStorage.from_url('redis://localhost:6379/0')
    dp = Dispatcher(storage=storage)

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.include_routers(
        user_router
    )

    db_users = Users(pool_connect)
    db_cart = Cart(pool_connect)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            users=db_users,
            cart=db_cart
        )
    except Exception as ex:
        logging.error(f'[!!! Exception] - {ex}', exc_info=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(start())
