from elasticsearch import Elasticsearch
from utils.config import ES_HOST, ES_INDEX
from utils.logger import Logger


class ElasticService:
    def __init__(self, es_client = None, index = None):
        self.es = Elasticsearch(es_client if es_client else ES_HOST)
        self.index = index if index else ES_INDEX
        self.logger = Logger.get_logger()

    def insert_one(self, record):
        try:
            return self.es.index(index=self.index, document=record)
        except Exception as e:
            self.logger.error(f"Error inserting record: {e}")
            return None
