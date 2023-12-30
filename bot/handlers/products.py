from aiogram import types

from .dispatcher import dp

@dp.callback_query_handler(regexp="product[0-9]+")
async def callback(c: types.CallbackQuery):
    pass