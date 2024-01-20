def initial_user(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": str(user["name"]),
        "email": user["email"],
        "image": user["image"],
        "password": user["password"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"],
    }

def list_users(users) -> list:
    return [initial_user(user) for user in users]


def initial_item(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": str(item["name"]),
        "description": item["description"],
        "image": item["image"],
        "price": item["price"],
        "stars": item["stars"],
        "created_at": item["created_at"],
        "updated_at": item["updated_at"],
    }

def list_items(items) -> list:
    return [initial_item(item) for item in items]