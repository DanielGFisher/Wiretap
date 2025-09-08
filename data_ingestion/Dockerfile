FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy data_ingestion code
COPY . .

# Mount data folder into container
VOLUME ["/data"]

# Default command to run the data_ingestion
CMD ["python", "main.py"]
