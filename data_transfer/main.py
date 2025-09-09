from kafka_reciever import KafkaConsumerClient

if __name__ == "__main__":
    consumer = KafkaConsumerClient()
    consumer.consume_loop()