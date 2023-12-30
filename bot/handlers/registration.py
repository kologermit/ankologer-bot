from aiogram import types

from db.models import Users
from .answers import Answers
from .dispatcher import dp
from db.logic import get_user

async def registration_name(u: Users, m: types.Message):
    m.text = m.text[:100]
    await u.update_from_dict({"name": m.text, "state": "registration:email"})
    await m.answer(Answers.registration_name.format(name=m.text),
        reply_markup=types.InlineKeyboardMarkup(1).add(
            types.InlineKeyboardButton(Answers.registration_name_error, callback_data="registration:name:error")))
    return True

@dp.callback_query_handler(text="registration:name:error")
async def callback(c: types.CallbackQuery):
    await c.answer()
    await c.message.delete()
    user = await get_user(c)
    if user.state in ["registration:name", "registration:email", "registration:phone", "registration:confirm"]:
        await user.update_from_dict({"state": "registration:name"})
        await user.save()
        await dp.bot.send_message(user.tg_id, Answers.registration_name_resend)
    return

# async def registration_email(u: Users, m: types.Message):
#     m.text = m.text[:400]