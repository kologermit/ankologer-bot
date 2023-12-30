from aiogram import executor

from db import init as db_init
from logger import setup_logger
from notify_admins import notify_admins
from dispatcher import dp
from handlers import *

async def on_startup(_):
    setup_logger()
    await db_init()
    await notify_admins()

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
