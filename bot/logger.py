import logging, datetime, os, sys
from aiogram import types

def setup_logger():
    now = datetime.datetime.now()

    if not os.path.exists("logs"):
        os.makedirs("logs")

    logging_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(filename="logs/{year}-{month}-{day}-{hour}-{minute}-{second}.txt".format(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=now.hour,
        minute=now.minute,
        second=now.second
    ), format=logging_format)
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(logging_format)
    handler.setFormatter(formatter)
    root.addHandler(handler)

def log_message(m: types.Message, state: str = ""):
    logging.info("Type: Message; Id: {user_id}; Name: {user_name}; Username: @{username}; State: {state}; Text: {text}; ContentType: {content_type}".format(
        user_id=m.from_user.id,
        user_name=m.from_user.full_name,
        username=m.from_user.username,
        state=state,
        text=str(m.text),
        content_type=m.content_type
    ))