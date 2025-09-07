from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class ElasticService:
    def __init__(self, es_client, index):
        self.es = es_client
        self.index = index

    def insert_one(self, record):
        return self.es.index(index=self.index, document=record)