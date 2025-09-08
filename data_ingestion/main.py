from processor import Processor
from load_data import DataLoader
from kafka_sender import KafkaProducerClient

data_loader = DataLoader()

processor = Processor()

kafka_producer = KafkaProducerClient()

data = processor.data

for file in data_loader.wav_files:
    processor.create_json_object(file)

kafka_producer.send("Audio-JSON", data)
