import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

AUDIO_URL = os.getenv("AUDIO_URL", r"C:\Users\danie\Downloads\podcasts-20250907T074751Z-1-001\podcasts")
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27107")
MONGO_DB = os.getenv("MONGO_DB", "audio_db")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "files")
ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")
ES_INDEX = os.getenv("ES_INDEX", "audio_logs")