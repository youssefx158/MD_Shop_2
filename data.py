import json
import os

DATA_FILE = os.path.join("data", "products.json")

def load_products():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_products(products):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

def add_product(product):
    products = load_products()
    product_id = str(len(products) + 1)
    product["id"] = product_id
    products[product_id] = product
    save_products(products)
    return product_id

def check_login(email, password):
    # مثال على حساب أدمن ثابت
    if email == "admin@mdshop.com" and password == "admin123":
        return True, "admin"
    return False, "بيانات الدخول غير صحيحة."
