.
├── README.md
├── data_ingestion
│ ├── Dockerfile
│ ├── __pycache__
│ ├── kafka_sender.py
│ ├── load_data.py
│├── main.py
│ ├── processor.py
│ └── requirements.txt
├── data_transfer
│ ├── Dockerfile
│ ├── __pycache__
│ ├── elastic_service.py
│ ├── hasher.py
│ ├── kafka_reciever.py
│ ├── main.py
│ ├── mongo_service.py
│ └── requirements.txt
├── docker-compose.yaml
└── utils
    ├── __pycache__
    ├── config.py
    └── logger.py
