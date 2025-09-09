from pymongo import MongoClient
from gridfs import GridFS
from utils.config import MONGO_URI, MONGO_DB, MONGO_COLLECTION
from data_transferal.hasher import Hasher
from utils.logger import Logger


class MongoService:
    def __init__(self, uri= None, db_name = MONGO_DB, collection_name = MONGO_COLLECTION):
        self.client = MongoClient(uri or MONGO_URI)
        self.db = self.client.db_name
        self.collection = self.db[collection_name]
        self.fs = GridFS(self.db)
        self.logger = Logger.get_logger()

    def store_wav_file(self, path):
        file_id = None
        try:
            with open(path, 'rb') as f:
                file_data = f.read()
                file_id = self.fs.put(file_data, filename=Hasher().generate_file_hash(path), content_type='audio/wav')
        except Exception as e:


    def insert(self, record):
        self.collection.insert_one(record)

    def close(self):
        self.client.close()