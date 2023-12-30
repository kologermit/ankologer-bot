import os, json

try:
    from .env import *
    token = token
    admins = admins
    prodamus = prodamus
except:
    token = os.getenv("TOKEN", "5469643644:AAGswk4CVHLOTVx6ZwsVglcKcxkLQeMd030")
    admins = json.loads(f"[{os.getenv('ADMINS', '847721936')}]")
    prodamus = {
        "token": os.getenv("PRODAMUS_TOKEN", ""),
        "url": os.getenv("PRODAMUS_URL", ""),
        "demo_mode": 1,
    }