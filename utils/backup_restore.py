import os
import json
from config import db

BACKUP_PATH = "backup/"

def backup_all():
    if not os.path.exists(BACKUP_PATH):
        os.makedirs(BACKUP_PATH)
    for name in db.list_collection_names():
        data = list(db[name].find())
        with open(f"{BACKUP_PATH}{name}.json", "w") as f:
            json.dump(data, f, default=str)

def restore_all():
    for name in db.list_collection_names():
        path = f"{BACKUP_PATH}{name}.json"
        if os.path.exists(path):
            with open(path) as f:
                data = json.load(f)
                db[name].delete_many({})
                db[name].insert_many(data)
