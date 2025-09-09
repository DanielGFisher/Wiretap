from confluent_kafka import Consumer, KafkaError
from utils.logger import Logger
from utils.config import KAFKA_BOOTSTRAP
from data_transfer.mongo_service import MongoService
from data_transfer.elastic_service import ElasticService
import json

class KafkaConsumerClient:
    def __init__(self, topic="Audio-JSON", group_id="transfer-consumer"):
        self.consumer = Consumer({
            'bootstrap.servers': KAFKA_BOOTSTRAP,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        })
        self.consumer.subscribe([topic])
        self.mongo_service = MongoService()
        self.elastic_service = ElasticService()
        self.logger = Logger.get_logger()


    def consume_loop(self):
        while True:
            msg = self.consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() != KafkaError._PARTITION_EOF:
                    self.logger.error(f"Consumer error: {msg.error()}")
                continue
            try:
                json_data = json.loads(msg.value().decode('utf-8'))
                self.logger.info(f"Received message: {msg.value().decode('utf-8')}")
                self.mongo_service.insert_metadata(json_data)
                self.elastic_service.insert_one(json_data)
            except Exception as e:
                self.logger.error(f"Processing error occured: {e}")


# Test Usage
if __name__ == "__main__":
    kafka_consumer = KafkaConsumerClient("Audio-JSON")
    kafka_consumer.consume_loop()