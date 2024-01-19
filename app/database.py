from pymongo import MongoClient
from .config import settings

connect = MongoClient(f"mongodb+srv://{settings.database_username}:{settings.database_password}@cluster0.gw8wj.mongodb.net/?retryWrites=true&w=majority")

db = connect.database

collection_users = db['users']

try:
    connect.admin.command('ping')
    print("Connection With MongoDB Successfully!!!")
except Exception as error:
    print(error)