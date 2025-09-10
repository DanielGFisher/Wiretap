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


    def store_wav_file(self, path):
        file_id = self.hasher.generate_file_hash(path)
        try:
            with open(path, 'rb') as f:
                file_data = f.read()
                existing = self.fs.find({"_id": file_id})
                for doc in existing:
                    self.fs.delete(doc._id)
                    self.fs.put(file_data, _id=file_id, filename=path.name, content_type="audio/wav")
                    self.logger.info(f"Stored file data with hashed id {file_id}!")
                    return file_id
        except Exception as e:
            self.logger.error(f"Mongo - Error storing: {e}")
        return None


    def insert_metadata(self, record):
        try:
            file_id = record.get("_id")
            if not file_id:
                self.logger.error(f"_id does not match {file_id}")
                return self.collection.update_one({"_id": file_id}, {"$set": record}, upsert=True)
        except Exception as e:
            self.logger.error(f"Mongo - Error inserting record: {e}")


    def close(self):
        self.client.close()