from aiogram import types
from .models import Users, Products

async def get_user(m: types.Message) -> Users:
    user = await Users.filter(tg_id=m.from_user.id).all()
    if len(user) == 0:
        user = await Users.create(
            tg_id=m.from_user.id,
            name=m.from_user.full_name,
            email="",
            phone="",
            verified=False,
            state="start"
        )
    else:
        user = user[0]
    return user

async def get_all_users():
    return await Users.filter().all()

async def get_products():
    return await Products.filter().all()
