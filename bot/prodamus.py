import requests, logging
from config import prodamus as prodamusConf

def prodamus_create_url(product: dict, extra: str, user, url):
    data = {
        "do": "link",
        "order_id": product["id"],
        "demo_mode": prodamusConf["demo_mode"],
        "customer_extra": extra,
        "currency": "rub",
        "urlSuccess": url,
        "payments_limit": 1,
        "_param_user_tg_id": user.id,
        "_param_user_name": str(user.full_name),
        "_param_user_username": str(user.username),
        "_param_product_id": product["id"],
        "payments_limit": "1",
    }
    logging.info(f"Prodamus data: {data}")
    for key, value in product.items():
        data[f"products[0][{key}]"] = value
    return requests.get(prodamusConf["url"], data).text
