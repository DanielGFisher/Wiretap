from processor import Processor
from load_data import DataLoader
from kafka_sender import KafkaProducerClient

data_loader = DataLoader()

processor = Processor(data_loader.wav_files)

kafka_producer = KafkaProducerClient()

data = processor.data

kafka_producer.send("Audio-JSON", data)
