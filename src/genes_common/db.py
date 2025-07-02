from pymongo import MongoClient
from .config import settings

_mongo_client = None

def get_mongo_client():
    global _mongo_client
    if _mongo_client is None:
        print("settings.MONGODB_URI", settings.MONGODB_URI)
        _mongo_client = MongoClient(settings.MONGODB_URI)
    return _mongo_client


def get_mongo_db():
    return get_mongo_client()[settings.MONGODB_DATABASE]
