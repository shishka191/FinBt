import json
import os

DB_PATH = "users_data.json"

def load_db():
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as f:
            json.dump({}, f)
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f)

def get_user_data(user_id):
    db = load_db()
    user_id = str(user_id)
    if user_id not in db:
        db[user_id] = {"income": 0, "expense": 0}
        save_db(db)
    return db[user_id]

def update_user_data(user_id, amount, mode):
    db = load_db()
    user_id = str(user_id)
    if user_id not in db:
        db[user_id] = {"income": 0, "expense": 0}
    db[user_id][mode] += amount
    save_db(db)