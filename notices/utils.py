from pymongo import MongoClient
from django.conf import settings
import certifi

def get_db_handle():
    client = MongoClient(settings.MONGO_URI, tlsCAFile=certifi.where())
    db = client[settings.MONGO_DB_NAME]
    return db, client
