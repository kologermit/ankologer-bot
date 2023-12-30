from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import token

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot, storage=MemoryStorage())
