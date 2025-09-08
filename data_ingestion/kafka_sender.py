from confluent_kafka import Producer
from data_ingestion.config import KAFKA_BOOTSTRAP
from utils.logger import Logger


class KafkaProducerClient:
    def __init__(self, bootstrap_servers=KAFKA_BOOTSTRAP):
        self.producer = Producer({'bootstrap.servers': bootstrap_servers})
        self.logger = Logger.get_logger()


    def delivery_report(self, err, msg):
        if err:
            self.logger.error(f"Message failed delivery: {err}")
        else:
            self.logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def send(self, topic, message):
        self.producer.produce(topic, value=message, callback=self.delivery_report)
        self.producer.flush()
        self.logger.info(f"Attempting to send message: {message} to topic: {topic}")