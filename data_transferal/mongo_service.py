from pymongo import MongoClient
from gridfs import GridFS
from data_transferal.hasher import Hasher


class MongoService:
    def __init__(self, uri= None, db_name = "audio_db", collection_name = "files"):
        self.client = MongoClient(uri or ["mongo://localhost:27107"])
        self.db = self.client.db_name
        self.collection = self.client[db_name][collection_name]
        self.fs = GridFS(self.db)

    def open_wav_file(self, path):
        with open(path, 'rb') as f:
            file_data = f.read()
            file_id = self.fs.put(file_data, filename=Hasher.generate_file_hash(path), content_type='audio/wav')

    def insert(self, record):
        self.collection.insert_one(record)

    def close(self):
        self.client.close()