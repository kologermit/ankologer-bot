from tortoise.models import Model
from tortoise import fields

class Users(Model):
    id = fields.IntField(pk=True)
    tg_id = fields.IntField()
    name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=400)
    phone = fields.CharField(max_length=12)
    verified = fields.BooleanField(default=False)
    state = fields.CharField(max_length=30, default="start")

class Messages(Model):
    id = fields.IntField(pk=True)
    time = fields.TimeField(auto_now=True)
    text = fields.TextField()
    user_id = fields.IntField()
    user_tg_id = fields.IntField()

