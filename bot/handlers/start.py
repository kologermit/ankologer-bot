from aiogram import types

from .answers import Answers
from db.models import Users
from db.logic import get_products

async def start(u: Users, m: types.Message) -> bool:
    await m.answer(Answers.start.format(name=u.name), 
        reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            types.KeyboardButton(Answers.yes),
            types.KeyboardButton(Answers.no)
        ))
    await u.update_from_dict({"state": "start:presentation"})
    return True

menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            types.KeyboardButton(Answers.Menu.registration_button),
            types.KeyboardButton(Answers.Menu.me_button),
            types.KeyboardButton(Answers.Menu.products_list_button)
        )

async def start_presentation(u: Users, m: types.Message) -> bool:
    if m.text == Answers.yes:
        await m.answer(Answers.Menu.presentation, reply_markup=types.InlineKeyboardMarkup(1).add(
            types.InlineKeyboardButton(text="Презентация", url=Answers.Menu.presentation_link)))
        await m.answer("Меню", reply_markup=menu_markup)
    else:
        await m.answer(Answers.Menu.menu, reply_markup=menu_markup)
    await u.update_from_dict({"state": "menu"})
    return True
    
async def menu(u: Users, m: types.Message) -> bool:
    if m.text == Answers.Menu.registration_button:
        await m.answer(Answers.Registration.send_name, reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            types.KeyboardButton(Answers.back)
        ))
        await u.update_from_dict({"state": "registration:name"})
        return True
    if m.text == Answers.Menu.me_button:
        await m.answer(Answers.Menu.presentation, reply_markup=types.InlineKeyboardMarkup(1).add(
            types.InlineKeyboardButton(text="Презентация", url=Answers.Menu.presentation_link)))
        return True
    if m.text == Answers.Menu.products_list_button:
        products = await get_products()
        buttons = []
        for p in products:
            await m.answer(Answers.Products.product.format(
                id=p.id,
                name=p.name,
                description=p.description,
                price=p.price
            ))
            buttons.append(types.KeyboardButton(str(p.id)))
        if not u.verified:
            await m.answer(Answers.Products.no_verified)
            return True
        buttons.append(types.KeyboardButton(Answers.back))
        await u.update_from_dict({"state": "products:select"})
        await m.answer(Answers.Products.menu, reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            *buttons))
        return True
    return False