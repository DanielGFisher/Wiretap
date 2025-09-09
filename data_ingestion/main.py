from processor import Processor
from utils.load_data import DataLoader
from kafka_sender import KafkaProducerClient

if __name__ == "__main__":
    data_loader = DataLoader()
    processor = Processor()
    kafka_producer = KafkaProducerClient()

    for file in data_loader.wav_files:
        data = processor.create_json_object(file)
        if data:
            kafka_producer.send("Audio-JSON", data)

