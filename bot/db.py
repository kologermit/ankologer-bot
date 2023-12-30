from tortoise import Tortoise
from tortoise.models import Model
from tortoise import fields

db = Tortoise()

async def init():
    await Tortoise.init(db_url='sqlite://db.sqlite3', modules={'models': ['db']})
    await Tortoise.generate_schemas()

async def on_shutdown():
    await db.close_connections()

class Users(Model):
    id = fields.IntField(pk=True)
    tg_id = fields.IntField()
    first_name = fields.CharField(max_length=100)
    second_name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=400)
    phone = fields.CharField(max_length=12)
    verified = fields.BooleanField(default=False)
    state = fields.CharField(max_length=15, default="menu")

class Messages(Model):
    id = fields.IntField(pk=True)
    time = fields.TimeField(auto_now=True)
    text = fields.TextField()
    user_id = fields.IntField()
    user_tg_id = fields.IntField()
    answer = fields.TextField()