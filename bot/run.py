from aiogram import executor

from db.init import init as db_init
from logger import setup_logger
from handlers.notify_admins import notify_admins
from handlers.init import dp
from webhook import setup_webhook

async def main(_):
    setup_logger()
    await setup_webhook()
    await db_init()
    await notify_admins()

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=main)
