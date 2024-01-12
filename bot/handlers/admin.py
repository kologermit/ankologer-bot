from aiogram import types
import openpyxl, logging, os

from .dispatcher import dp
from .answers import Answers
from .start import menu_markup
from config import admins
from db.models import Users, Products
from db.logic import get_user, get_all_users

@dp.message_handler(commands=["admin"])
async def handler(m: types.Message):
    if m.from_user.id not in admins:
        return
    await m.answer(Answers.Admin.menu, reply_markup=types.InlineKeyboardMarkup(1).add(
        types.InlineKeyboardButton("Загрузить товары", callback_data="admin:load_products"),
        types.InlineKeyboardButton("Рассылка сообщения", callback_data="admin:mailing"),
    ))

@dp.callback_query_handler(text="admin:load_products")
async def callback(c: types.CallbackQuery):
    user = await get_user(c)
    await user.update_from_dict({"state": "load_products"})
    await user.save()
    await c.message.answer(Answers.Admin.load_products)
    await c.message.delete()

@dp.callback_query_handler(text="admin:mailing")
async def callback(c: types.CallbackQuery):
    user = await get_user(c)
    await user.update_from_dict({"state": "mailing"})
    await user.save()
    await c.message.answer(Answers.Admin.mailing)
    await c.message.delete()

async def mailing_text(u: Users, m: types.Message, users: list[Users]):
    for user in users:
        try:
            await dp.bot.send_message(user.tg_id, m.text)
        except Exception as err:
            logging.info("User: Id: {id}; Name: {name}".format(id=user.tg_id, name=user.name))
            logging.exception(err)

async def mailing_document(u: Users, m: types.Message, users: list[Users]):
    if not os.path.exists("tmp/"):
        os.mkdir("tmp")
    file_name = f"tmp/{m.document.file_name}"
    if os.path.exists(file_name):
        os.remove(file_name)
    file = await dp.bot.get_file(m.document.file_id)
    await dp.bot.download_file(file.file_path, file_name)
    for user in users:
        try:
            await dp.bot.send_document(user.tg_id, open(file_name, "rb"))
        except Exception as err:
            logging.info("User: Id: {id}; Name: {name}".format(id=user.tg_id, name=user.name))
            logging.exception(err)

async def mailing_voice(u: Users, m: types.Message, users: list[Users]):
    if not os.path.exists("tmp/"):
        os.mkdir("tmp")
    file = await m.voice.download(destination_dir="tmp")
    file_name = file.name
    file.close()
    for user in users:
        try:
            await dp.bot.send_voice(user.tg_id, open(file_name, "rb"))
        except Exception as err:
            logging.info("User: Id: {id}; Name: {name}".format(id=user.tg_id, name=user.name))
            logging.exception(err)

async def mailing_video_note(u: Users, m: types.Message, users: list[Users]):
    if not os.path.exists("tmp/"):
        os.mkdir("tmp")
    file = await m.video_note.download(destination_dir="tmp")
    file_name = file.name
    file.close()
    for user in users:
        try:
            await dp.bot.send_video_note(user.tg_id, open(file_name, "rb"))
        except Exception as err:
            logging.info("User: Id: {id}; Name: {name}".format(id=user.tg_id, name=user.name))
            logging.exception(err)

async def mailing_photo(u: Users, m: types.Message, users: list[Users]):
    if not os.path.exists("tmp/"):
        os.mkdir("tmp")
    file = await m.photo[-1].download(destination_dir="tmp")
    file_name = file.name
    file.close()
    for user in users:
        try:
            await dp.bot.send_photo(user.tg_id, open(file_name, "rb"))
        except Exception as err:
            logging.info("User: Id: {id}; Name: {name}".format(id=user.tg_id, name=user.name))
            logging.exception(err)

async def mailing(u: Users, m: types.Message) -> bool:
    mailing_message = await m.answer("Начинаю отправку")
    types = {
        "text": mailing_text,
        "document": mailing_document,
        "voice": mailing_voice,
        "video_note": mailing_video_note,
        "photo": mailing_photo
    }
    if types.get(m.content_type) is None:
        await m.answer("Тип сообщения не найден")
        return
    try:
        users = await get_all_users()
        await types[m.content_type](u, m, users)
        await dp.bot.edit_message_text(
            "Рассылка успешно окончена",
            chat_id=m.chat.id,
            message_id=mailing_message.message_id,
        )
    except Exception as err:
        logging.exception(err)
        await m.answer(err)
        await dp.bot.edit_message_text(
            "При загрузке базы сообщений произошла ошибка. Проверьте структуру файла и повторите попытку.",
            chat_id=m.chat.id,
            message_id=mailing_message.message_id,
        )
    await u.update_from_dict({"state": "menu"})
    await m.answer(Answers.Menu.menu, reply_markup=menu_markup)
    return True

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
        logging.exception(e)
        await m.answer(e)
        await dp.bot.edit_message_text(
            "При загрузке базы сообщений произошла ошибка. Проверьте структуру файла и повторите попытку.",
            chat_id=m.chat.id,
            message_id=load_message.message_id,
        )
    await m.answer(Answers.Menu.menu, reply_markup=menu_markup)
    await u.update_from_dict({"state": "menu"})
    return True