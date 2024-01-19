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