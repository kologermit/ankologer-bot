from config import admins
from dispatcher import dp
import logging

async def notify_admins():
    for admin in admins:
        try:
            await dp.bot.send_message(admin, "Start AnKologer Bot")
        except Exception as err:
            logging.exception(err)