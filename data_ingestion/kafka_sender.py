import os
from confluent_kafka import Producer
from data_ingestion.config import KAFKA_BOOTSTRAP


class KafkaProducerClient:
    def __init__(self, bootstrap_servers=KAFKA_BOOTSTRAP):
        self.producer = Producer({'bootstrap.servers': bootstrap_servers})

    def delivery_report(self, err, msg):
        if err:
            print(f"Message failed delivery: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def send(self, topic, message):
        self.producer.produce(topic, value=message, callback=self.delivery_report)
        self.producer.flush()