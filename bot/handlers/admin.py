from aiogram import types

from .dispatcher import dp
from config import admins

@dp.message_handler(commands=["admin"])
async def admin(m: types.Message):
    if m.from_user.id not in admin:
        return
    