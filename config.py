from pymongo import MongoClient

try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    client.server_info()  # Force connection
    db = client["billing_soft_pro"]

    # Collections
    users_collection = db["users"]
    products_collection = db["products"]
    customers_collection = db["customers"]
    vendors_collection = db["vendors"]
    invoices_collection = db["invoices"]

except Exception as e:
    print("❌ Could not connect to MongoDB:", e)
    users_collection = products_collection = customers_collection = vendors_collection = invoices_collection = None
