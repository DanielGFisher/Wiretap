import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

AUDIO_URL = os.getenv("AUDIO_URL", r"C:\Users\danie\Downloads\podcasts-20250907T074751Z-1-001\podcasts")
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")

