from models.user import register_user

if register_user("admin", "admin123", role="Admin"):
    print("✅ User 'admin' created")
else:
    print("⚠️ User already exists")
