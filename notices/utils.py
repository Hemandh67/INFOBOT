from pymongo import MongoClient
from django.conf import settings

def get_db_handle():
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]
    return db, client
