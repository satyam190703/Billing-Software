# seed_admin.py

from models.user import register_user

if register_user("admin", "admin123", "Admin"):
    print("Admin user created.")
else:
    print("Admin already exists.")
