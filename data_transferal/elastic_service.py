from elasticsearch import Elasticsearch

from utils.logger import Logger


class ElasticService:
    def __init__(self, es_client = None, index = "audio_logs"):
        self.es = Elasticsearch(es_client or ["http://localhost:9200"])
        self.index = index
        self.logger = Logger.get_logger()

    def insert_one(self, record):
        self.logger.info(f"Sending record {record} to Elastic")
        return self.es.index(index=self.index, document=record)