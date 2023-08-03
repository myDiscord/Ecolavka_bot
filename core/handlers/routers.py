from aiogram import Router

from core.handlers.start import router as start
from core.handlers.registration import router as registration
from core.handlers.account import router as account
from core.handlers.connection import router as connection
from core.handlers.delivery import router as delivery
from core.handlers.news import router as news
from core.handlers.catalog import router as catalog
from core.handlers.cart import router as cart
from core.handlers.pay import router as pay


user_router = Router()
user_router.include_routers(
    start,
    registration,
    account,
    connection,
    delivery,
    news,
    catalog,
    cart,
    pay
)
