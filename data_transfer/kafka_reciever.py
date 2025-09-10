from confluent_kafka import Consumer, KafkaError
from utils.logger import Logger
from utils.config import KAFKA_BOOTSTRAP, ES_INDEX
from data_transfer.mongo_service import MongoService
from data_transfer.elastic_service import ElasticService
from data_transfer.hasher import Hasher
import json
import signal
import sys


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
        self.hasher = Hasher()
        self.logger = Logger.get_logger()
        self._ensure_index_mapping()

    def _ensure_index_mapping(self):
        """
        Instantiates mapping for incoming data
        """
        mapping = {
            "mappings": {
                "properties": {
                    "wav_file_link": {"type": "keyword"},
                    "metadata": {
                        "properties": {
                            "file_name": {"type": "keyword"},
                            "date_of_creation": {"type": "date"},
                            "size": {"type": "long"}
                        }
                    },
                    "text": {
                        "properties": {
                            "content": {"type": "text"},
                            "bds_percent": {"type": "float"},
                            "is_bds": {"type": "boolean"},
                            "bds_threat_level": {"type": "keyword"}
                        }
                    }
                }
            }
        }
        if not self.elastic_service.es.indices.exists(index=ES_INDEX):
            self.elastic_service.es.indices.create(index=ES_INDEX, body=mapping)
            self.logger.info(f"New index '{ES_INDEX}' created with mapping")

    def consume_loop(self):
        self.logger.info("Kafka consumer started. Waiting for messages...")
        try:
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
                    self.logger.info(f"Received message: {json_data}")

                    wav_path = json_data.get("wav_file_link")
                    if not wav_path:
                        self.logger.error("No WAV file in consumed data!")
                        continue

                    file_id = self.hasher.generate_file_hash(wav_path)
                    self.mongo_service.insert_metadata(json_data)

                    data = {
                        "wav_file_link": str(wav_path),
                        "metadata": json_data.get("metadata", {}),
                        "text": json_data.get("text", {})
                    }

                    self.elastic_service.es.index(index=ES_INDEX, id=file_id, body=data)
                    self.logger.info(f"Indexed document with ID {file_id}")

                except Exception:
                    self.logger.exception("Processing error occurred")

        finally:
            self.logger.info("Closing Kafka consumer...")
            self.consumer.close()


# Test Usage
if __name__ == "__main__":
    consumer = KafkaConsumerClient("Audio-JSON")
    consumer.consume_loop()
