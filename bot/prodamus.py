import requests
from config import prodamus as prodamusConf

def prodamus_create_url(product: dict, extra: str, user):
    data = {
        "do": "link",
        "order_id": product["id"],
        "demo_mode": 1,
        "customer_extra": extra,
        "currency": "rub",
        "payments_limit": 1,
        "_param_user_tg_id": user.id,
        "_param_user_name": str(user.full_name),
        "_param_user_username": str(user.username),
        "_param_product_id": product["id"],
        "payments_limit": "1",
    }
    for key, value in product.items():
        data[f"products[0][{key}]"] = value
    return requests.get(prodamusConf["url"], data).text
