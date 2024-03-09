import requests, logging
from config import prodamus as prodamusConf
from aiogram import types

def prodamus_create_url(product: dict, extra: str, user: types.User, url):
    data = {
        "do": "link",
        "order_id": product["id"],
        "demo_mode": prodamusConf["demo_mode"],
        "customer_extra": "Описание",
        "currency": "rub",
        "urlSuccess": url,
        "_param_user_name": user.full_name,
        "_param_user_username": user.username,
        "_param_user_tg_id": user.id,
        "_param_product_id": product["id"],
        "_param_url_success": url,
    }
    logging.info(f"Prodamus data: {data}")
    for key, value in product.items():
        if len(str(value)) <= 150:
           data[f"products[0][{key}]"] = value
    return requests.get(prodamusConf["url"], data).text
