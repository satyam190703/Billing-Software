import bcrypt
from config import users_collection

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def register_user(username, password, role="Staff"):
    if users_collection.find_one({"username": username}):
        return {"status": "exists"}
    
    hashed = hash_password(password)
    users_collection.insert_one({
        "username": username,
        "password": hashed,
        "role": role
    })
    return {"status": "registered"}

def login_user(username, password):
    user = users_collection.find_one({"username": username})
    if not user:
        return {"status": "not_found"}
    
    if verify_password(password, user["password"]):
        return {"status": "success", "role": user["role"]}
    else:
        return {"status": "wrong_password"}
