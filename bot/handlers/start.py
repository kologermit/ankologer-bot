from aiogram import types
import logging

from .answers import Answers
from .dispatcher import dp
from db.models import Users
from db.logic import get_products
from prodamus import prodamus_create_url

async def start(u: Users, m: types.Message) -> bool:
    await m.answer(Answers.start.format(name=u.name), 
        reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            types.KeyboardButton(Answers.yes),
            types.KeyboardButton(Answers.no)
        ))
    await u.update_from_dict({"state": "start:presentation"})
    return True

menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            # types.KeyboardButton(Answers.Menu.registration_button),
            types.KeyboardButton(Answers.Menu.products_list_button),
            types.KeyboardButton(Answers.Menu.me_button),
        )

async def start_presentation(u: Users, m: types.Message) -> bool:
    if m.text == Answers.yes:
        await m.answer_photo(
            photo=open("photo.jpg", "rb"),
            reply_markup=menu_markup)
        await m.answer(text=Answers.Menu.presentation, 
            reply_markup=types.InlineKeyboardMarkup(1).add(
            types.InlineKeyboardButton(Answers.about_button, url=Answers.Menu.presentation_link)))
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
        await m.answer_photo(
            photo=open("photo.jpg", "rb"))
        await m.answer(text=Answers.Menu.presentation, 
            reply_markup=types.InlineKeyboardMarkup(1).add(
            types.InlineKeyboardButton(Answers.about_button, url=Answers.Menu.presentation_link)))
        return True
    if m.text == Answers.Menu.products_list_button:
        products = await get_products()
        for p in products:
            await m.answer(Answers.Products.product.format(
                name=p.name,
                price=p.price
            ), reply_markup=types.InlineKeyboardMarkup(2).add(
                types.InlineKeyboardButton("Описание", callback_data="description:more" + str(p.id)),
                types.InlineKeyboardButton("Купить", callback_data="product:buy" + str(p.id))
            ))
        return True
    return False

@dp.callback_query_handler(regexp="description:more[0-9]+")
async def callback(c: types.CallbackQuery):
    products = await get_products()
    p = None
    for product in products:
        if f"description:more{product.id}" == c.data:
            p = product
    if p is None:
        return
    await c.message.edit_text(Answers.Products.full.format(
        name=p.name,
        description=p.description,
        price=p.price
    ), reply_markup=types.InlineKeyboardMarkup(1).add(
        types.InlineKeyboardMarkup(text="Уменьшить", callback_data="description:less" + str(p.id)),
        types.InlineKeyboardButton(text="Купить", callback_data="product:buy" + str(p.id))
    ))

@dp.callback_query_handler(regexp="description:less[0-9]+")
async def callback(c: types.CallbackQuery):
    products = await get_products()
    p = None
    for product in products:
        if f"description:less{product.id}" == c.data:
            p = product
    if p is None:
        return
    await c.message.edit_text(Answers.Products.product.format(
        name=p.name,
        price=p.price
    ), reply_markup=types.InlineKeyboardMarkup(2).add(
        types.InlineKeyboardMarkup(text="Описание", callback_data="description:more" + str(p.id)),
        types.InlineKeyboardButton(text="Купить", callback_data="product:buy" + str(p.id))
    ))

@dp.callback_query_handler(regexp="product:buy")
async def callback(c: types.CallbackQuery):
    products = await get_products()
    p = None
    for product in products:
        if f"product:buy{product.id}" == c.data:
            p = product
    if p is None:
        return
    url = prodamus_create_url({
        "id": p.id,
        "name": p.name,
        "price": p.price,
        "quantity": 1,
        "sku": p.price
    }, p.description, c.from_user, p.url)
    await c.message.answer(f"<b>{p.name}</b>", reply_markup=types.InlineKeyboardMarkup(1).add(
        types.InlineKeyboardButton("Ссылка на оплату", url=url)
    ))
    await c.answer()
