import pymongo
import os


class db:
    def __init__(self):
        self.config = {
            "host": os.getenv("MONGO_HOST", "localhost"),
            "port": int(os.getenv("MONGO_PORT", "27017")),
            "username": os.getenv("MONGO_USER", "admin"),
            "password": os.getenv("MONGO_PASSWORD", "0000"),
            "authSource": os.getenv("MONGO_AUTH_SOURCE", "admin"),
        }
        self.db_name = os.getenv("MONGO_DB", "threat_db")
        self.client = None

    def get_connection(self):
        if self.client is None:
            self.client = pymongo.MongoClient(
                **self.config
            )
        return self.client

    def insert_to_top_threats(self, data_coll: list[dict]):
        client = self.get_connection()
        database = client[self.db_name]
        collection = database["top_threats"]
        collection.insert_many(data_coll)