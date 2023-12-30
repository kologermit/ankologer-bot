from aiogram import types

from .answers import Answers
from db.models import Users

async def start(u: Users, m: types.Message) -> bool:
    await m.answer(Answers.start.format(name=u.name))
    await u.update_from_dict({"state": "registration:name"})
    return True
        