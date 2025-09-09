from elasticsearch import Elasticsearch

class ElasticService:
    def __init__(self, es_client = None, index = "audio-index"):
        self.es = Elasticsearch(es_client or ["http://localhost:9200"])
        self.index = index

    def insert_one(self, record):
        return self.es.index(index=self.index, document=record)