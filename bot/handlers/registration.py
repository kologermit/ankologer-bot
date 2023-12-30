from aiogram import types
import re, phonenumbers

from db.models import Users
from .answers import Answers
from .dispatcher import dp
from db.logic import get_user
from .start import menu_markup

async def registration_name(u: Users, m: types.Message):
    m.text = m.text[:100]
    if m.text == Answers.back:
        await m.answer(Answers.Registration.invalid, reply_markup=menu_markup)
        await u.update_from_dict({"state": "menu"})
        return True
    await u.update_from_dict({"name": m.text, "state": "registration:email"})
    await m.answer(Answers.Registration.name.format(name=m.text),
        reply_markup=types.InlineKeyboardMarkup(1).add(
            types.InlineKeyboardButton(Answers.Registration.name_error, callback_data="registration:name:error")))
    return True

@dp.callback_query_handler(text="registration:name:error")
async def callback(c: types.CallbackQuery):
    await c.message.delete()
    user = await get_user(c)
    if user.state in ["registration:email", "registration:phone", "registration:confirm"]:
        await user.update_from_dict({"state": "registration:name"})
        await user.save()
        await dp.bot.send_message(user.tg_id, Answers.Registration.name_resend)

def is_valid_email(email: str) -> bool:
    return re.compile(r"[^@]+@[^@]+\.[^@]+").match(email)

async def registration_email(u: Users, m: types.Message):
    m.text = m.text[:400]
    if not is_valid_email(m.text):
        await m.answer(Answers.Registration.invalid_email.format(email=m.text))
        return True
    await u.update_from_dict({"email": m.text, "state": "registration:phone"})
    await m.answer(Answers.Registration.email.format(email=m.text), reply_markup=types.InlineKeyboardMarkup(1).add(
            types.InlineKeyboardButton(Answers.Registration.email_error, callback_data="registration:email:error")))
    return True

@dp.callback_query_handler(text="registration:email:error")
async def callback(c: types.CallbackQuery):
    await c.message.delete()
    user = await get_user(c)
    if user.state in ["registration:phone", "registration:confirm"]:
        await user.update_from_dict({"state": "registration:email"})
        await user.save()
        await dp.bot.send_message(user.tg_id, Answers.Registration.email_resend)

def is_valid_phone(phone: str) -> bool:
    try:
        phonenumbers.parse(phone)
        return True
    except:
        return False
    
def only_numbers(l: str) -> str:
    ans = ''
    for s in l:
        if s.isdigit() or s == "+":
            ans += s
    return ans

async def registration_phone(u: Users, m: types.Message):
    phone = only_numbers(m.text)[:20]
    if not is_valid_phone(phone):
        await m.answer(Answers.Registration.invalid_phone.format(phone=phone))
        return True
    await u.update_from_dict({"phone": phone, "state": "registration:confirm"})
    await m.answer(Answers.Registration.phone.format(name=u.name, email=u.email, phone=phone), 
        reply_markup=types.InlineKeyboardMarkup(1).add(
            types.InlineKeyboardButton(Answers.correct, callback_data="registration:correct"),
            types.InlineKeyboardButton(Answers.invalid, callback_data="registration:invalid"),
            types.InlineKeyboardButton(Answers.Registration.phone_error, callback_data="registration:phone:error")
            ))
    return True

@dp.callback_query_handler(text="registration:phone:error")
async def callback(c: types.CallbackQuery):
    await c.message.delete()
    user = await get_user(c)
    if user.state == "registration:confirm":
        await user.update_from_dict({"state": "registration:phone"})
        await user.save()
        await dp.bot.send_message(user.tg_id, Answers.Registration.phone_resend)

@dp.callback_query_handler(text="registration:correct")
async def callback(c: types.CallbackQuery):
    await c.message.delete()
    user = await get_user(c)
    await c.message.answer(Answers.Registration.correct, reply_markup=menu_markup)
    await user.update_from_dict({"state": "menu", "verified": True})
    await user.save()

@dp.callback_query_handler(text="registration:invalid")
async def callback(c: types.CallbackQuery):
    await c.message.delete()
    user = await get_user(c)
    await c.message.answer(Answers.Registration.invalid, reply_markup=menu_markup)
    await user.update_from_dict({"state": "menu"})
    await user.save()