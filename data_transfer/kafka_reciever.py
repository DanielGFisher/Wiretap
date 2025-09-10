from importlib.metadata import metadata

from confluent_kafka import Consumer, KafkaError
from speech_recognition.recognizers.whisper_api.base import logger

from data_transfer.hasher import Hasher
from utils.logger import Logger
from utils.config import KAFKA_BOOTSTRAP, ES_INDEX
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
                            "size": {"type": "ng"}
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
        if not self.elastic_service.es.indicies.exists(index=ES_INDEX):
            self.elastic_service.es.indicies.create(index=ES_INDEX, mapping=mapping)
            self.logger.info(f"New index created with mapping")

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

                wav_path = json_data["wav_file_link"]
                if not wav_path.exists():
                    self.logger.error("No WAV file in consumed data!")
                    continue

                file_id = self.hasher.generate_file_hash(wav_path)
                self.mongo_service.insert_metadata(json_data)

                data = {
                    "_id": file_id,
                    "wav_file_link": str(wav_path),
                    "metadata": json_data.get("metadata",{}),
                    "text": json_data.get("text", {})
                }
                self.elastic_service.es.index(index=ES_INDEX, id=file_id,document=data)

            except Exception as e:
                self.logger.error(f"Processing error occurred: {e}")


# Test Usage
if __name__ == "__main__":
    kafka_consumer = KafkaConsumerClient("Audio-JSON")
    kafka_consumer.consume_loop()