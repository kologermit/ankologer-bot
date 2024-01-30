from aiogram import types
import logging

from .dispatcher import dp
from .start import start, start_presentation, menu, menu_markup
from .registration import registration_name, registration_email, registration_phone
from .admin import load_products, mailing
from .answers import Answers
from db.models import Users, Messages
from db.logic import get_user
from logger import log_message

@dp.message_handler(commands=['start', 'restart'])
async def handler(m: types.Message):
    user = await get_user(m)
    log_message(m, user.state)
    await start(user, m)
    await user.save()

@dp.message_handler(commands=['menu'])
async def handler(m: types.Message):
    user = await get_user(m)
    log_message(m, user.state)
    await user.update_from_dict({"state": "menu"})
    await m.answer(Answers.Menu.menu, reply_markup=menu_markup)
    await user.save()

@dp.message_handler(content_types=types.ContentTypes.ANY)
async def handler(m: types.Message):
    if m.text is not None:
        m.text = m.text.strip().replace("  ", " ").replace("\t", "").replace("\n", "")
    user = await get_user(m)
    log_message(m, user.state)
    await Messages.create(
        user_tg_id=user.tg_id,
        text=str(m.text),
        user_id=user.id
    )
    states = {
        "start": start,
        "start:presentation": start_presentation,
        "registration:name": registration_name,
        "registration:email": registration_email,
        "registration:phone": registration_phone,
        "menu": menu,
        "load_products": load_products,
        "mailing": mailing,
    }
    try:
        if states.get(user.state) is None:
            await m.answer(f"Состояние {user.state} не найдено")
            return
        if await states[user.state](user, m) == False:
            await m.answer("""Я бот, многое не знаю, но отвечу на часто задаваемые вопросы:
"Курс идет онлайн или можно заниматься в удобное время?"
Курс в записи, проходите и выполняйте задания в удобном темпе. На вопросы отвечаю, помогаю.

"Курс для продвинутых или всем по силам?"
Курс абсолютно для всех, любой уровень

"Нужны ли какие-то приложения или специальные программы?"
Показываю разные варианты под смартфон и под компьютер. Вы сами выберете то, что подходит под ваше оборудование. В основном это Телеграм

Остались вопросы? <a href="https://t.me/+jqXOt64xla02ZjJi"><b>СПРОСИТЕ ТУТ</b></a>""", parse_mode="HTML")
            return
        await user.save()
    except Exception as err:
        await m.answer("Произошла ошибка")
        logging.exception(err)
        return