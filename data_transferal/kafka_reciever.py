from confluent_kafka import Consumer, KafkaError
import threading
import time

class KafkaConsumerClient:
    def __init__(self, topic, group_id='my-group', bootstrap_servers='localhost:9092', check_interval=2):
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.check_interval = check_interval
        self.running = True

        self.consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        })

    def wait_for_topic(self):
        """Wait until the topic exists in Kafka before subscribing."""
        while True:
            metadata = self.consumer.list_topics(timeout=5)
            if self.topic in metadata.topics:
                print(f"Topic '{self.topic}' exists. Subscribing...")
                break
            print(f"Topic '{self.topic}' does not exist yet. Retrying in {self.check_interval}s...")
            time.sleep(self.check_interval)

    def consume_loop(self):
        self.wait_for_topic()
        self.consumer.subscribe([self.topic])

        while self.running:
            msg = self.consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() != KafkaError._PARTITION_EOF:
                    print(f"Consumer error: {msg.error()}")
                continue
            print(f"Received message: {msg.value().decode('utf-8')}")

    def start(self):
        threading.Thread(target=self.consume_loop, daemon=True).start()

    def stop(self):
        self.running = False
        self.consumer.close()


if __name__ == "__main__":
    kafka_consumer = KafkaConsumerClient("Audio-JSON")
    kafka_consumer.consume_loop()
    kafka_consumer.start()