# models/user.py

from config import users_collection
import bcrypt

def authenticate(username, password):
    user = users_collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode(), user['password']):
        return {"username": user["username"], "role": user["role"]}
    return None

def register_user(username, password, role="Staff"):
    if users_collection.find_one({"username": username}):
        return False  # Already exists
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    users_collection.insert_one({
        "username": username,
        "password": hashed_pw,
        "role": role
    })
    return True

def get_all_users():
    users = users_collection.find({}, {"password": 0})  # Hide passwords
    return list(users)

def delete_user(username):
    result = users_collection.delete_one({"username": username})
    return result.deleted_count > 0
