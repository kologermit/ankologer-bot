from aiogram import types
import logging

from dispatcher import dp
from logger import log_message

@dp.message_handler()
async def handler(m: types.Message):
    log_message(m, "menu")
    await m.answer(m.text)