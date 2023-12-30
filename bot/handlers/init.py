from aiogram import types
import logging

from .dispatcher import dp
from .start import start
from .registration import registration_name
from db.models import Users, Messages
from db.logic import get_user
from logger import log_message

@dp.message_handler()
async def handler(m: types.Message):
    m.text = m.text.strip().replace("  ", " ").replace("\t", "").replace("\n", "")
    user = await get_user(m)
    log_message(m, user.state)
    await Messages.create(
        user_tg_id=user.tg_id,
        text=m.text,
        user_id=user.id
    )
    states = {
        "start": start,
        "registration:name": registration_name
    }
    try:
        if states.get(user.state) is None:
            await m.answer(f"Состояние {user.state} не найдено")
            return
        if await states[user.state](user, m) == False:
            await m.answer("Не понял!")
            return
        await user.save()
    except Exception as err:
        await m.answer("Произошла ошибка")
        logging.exception(err)
        return