import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

AUDIO_URL = os.getenv("AUDIO_URL", r"C:\Users\danie\Downloads\podcasts-20250907T074751Z-1-001\podcasts")
NEUTRAL_WORDS = os.getenv("NEUTRAL_WORDS", r"C:\Users\danie\PycharmProjectsc\Wiretap\data\neutral_keywords.txt")
HOSTILE_WORDS = os.getenv("HOSTILE_WORDS", r"C:\Users\danie\PycharmProjectsc\Wiretap\data\negative_keywords.txt")
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "audio_db")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "files")
ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")
ES_INDEX = os.getenv("ES_INDEX", "audio_index")
