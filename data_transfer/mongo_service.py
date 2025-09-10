from pymongo import MongoClient
from gridfs import GridFS
from utils.config import MONGO_URI, MONGO_DB, MONGO_COLLECTION
from data_transfer.hasher import Hasher
from utils.logger import Logger


class MongoService:
    def __init__(self, uri=None, db_name=MONGO_DB, collection_name=MONGO_COLLECTION):
        self.client = MongoClient(uri or MONGO_URI)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.fs = GridFS(self.db)
        self.logger = Logger.get_logger()
        self.hasher = Hasher()

    def insert_metadata(self, record):
        try:
            file_id = record.get("_id")
            if not file_id:
                self.logger.error("Record is missing '_id'")
                return None
            return self.collection.update_one({"_id": file_id}, {"$set": record}, upsert=True)
        except Exception as e:
            self.logger.error(f"Mongo - Error inserting record: {e}")
            return None

    def close(self):
        self.client.close()