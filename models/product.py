# Product schema & operations
from config import products_collection

def add_product(name, sku, price, quantity, gst_rate=0):
    products_collection.insert_one({
        "name": name,
        "sku": sku,
        "price": price,
        "quantity": quantity,
        "gst_rate": gst_rate
    })

def get_all_products():
    return list(products_collection.find())

def update_stock(sku, sold_qty):
    products_collection.update_one(
        {"sku": sku},
        {"$inc": {"quantity": -sold_qty}}
    )
