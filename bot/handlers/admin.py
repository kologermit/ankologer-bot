from aiogram import types
import openpyxl

from .dispatcher import dp
from .answers import Answers
from .start import menu_markup
from config import admins
from db.models import Users, Products
from db.logic import get_user

@dp.message_handler(commands=["admin"])
async def handler(m: types.Message):
    if m.from_user.id not in admins:
        return
    await m.answer(Answers.Admin.menu, reply_markup=types.InlineKeyboardMarkup(1).add(
        types.InlineKeyboardButton("Загрузить товары", callback_data="admin:load_products"),
    ))

@dp.callback_query_handler(text="admin:load_products")
async def callback(c: types.CallbackQuery):
    user = await get_user(c)
    await user.update_from_dict({"state": "load_products"})
    await user.save()
    await c.message.answer(Answers.Admin.load_products)
    await c.message.delete()

async def load_products(u: Users, m: types.Message) -> bool:
    load_message = await m.answer("Началась загрузка базы сообщений...")
    try:
        await Products.all().delete()
        file = await dp.bot.get_file(m.document.file_id)
        await dp.bot.download_file(file.file_path, "tmp.xlsx")
        wb = openpyxl.load_workbook("tmp.xlsx")
        sheet = wb.active
        for cells in sheet.iter_rows():
            items = [("-" if cell.value is None else cell.value) for cell in cells]
            while len(items) < 3:
                items.append("-")
            name, description, price, url = items
            price = int(price)
            await Products.create(name=name, description=description, price=price, url=url)
        await dp.bot.edit_message_text(
            "Отлично товары загружены!",
            chat_id=m.chat.id,
            message_id=load_message.message_id,
        )
    except Exception as e:
        await m.answer(e)
        await dp.bot.edit_message_text(
            "При загрузке базы сообщений произошла ошибка. Проверьте структуру файла и повторите попытку.",
            chat_id=m.chat.id,
            message_id=load_message.message_id,
        )
    await m.answer(Answers.Menu.menu, reply_markup=menu_markup)
    await u.update_from_dict({"state": "menu"})
    return True