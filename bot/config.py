import os, json

token = "5469643644:AAGswk4CVHLOTVx6ZwsVglcKcxkLQeMd030"
admins = [847721936]
prodamus = {
    "token": "",
    "url": "https://testpage7.payform.ru",
    "demo_mode": "1"
}

try:
    from .env import *
    token = env_token
    admins = env_admins
    prodamus = env_prodamus
except:
    token = os.getenv("TOKEN", "5469643644:AAGswk4CVHLOTVx6ZwsVglcKcxkLQeMd030")
    admins = json.loads(f"[{os.getenv('ADMINS', '847721936')}]")
    prodamus = {
        "token": os.getenv("PRODAMUS_TOKEN", ""),
        "url": os.getenv("PRODAMUS_URL", ""),
        "demo_mode": os.getenv("PRODAMUS_DEMO_MODE", "1"),
    }