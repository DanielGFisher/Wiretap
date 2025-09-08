import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

AUDIO_URL = os.getenv("AUDIO_URL", "/data")
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "host.docker.internal:9092")

