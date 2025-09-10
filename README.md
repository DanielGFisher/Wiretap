# Wiretap

This Wiretap project instantiates a pipeline that loads WAV files, 
builds a JSON bject that describes them in a very basic manner 
and proceeds to send them through Kafka to MongoDB and Elasticsearch respectively.
All the while it runs logs for each process completed and sends them to an Elasticsearch Index.

The project is split into two parts as follows;

 ## Data Ingestion

This phase handles the loading of the WAV file paths from a local folder, before going through a process
of getting the file name, date of creation, size and extracts the text from the audio file and creates a JSON
object with all the aforementioned processes. It also handles the sentiment and BDS processing.

### Build:
```bach

├── data_ingestion
│ ├── Dockerfile - Containerizes application
│ ├── kafka_sender.py - Deals with the Kafka Producer
│ ├── load_data.py - Deals with the loading of the files from the 
│ │                  folder and the loading of file paths to a list
│ ├── main.py - Runs the program
│ ├── processor.py - Deals with processing the files into a JSON object
│ └── requirements.txt - Holds requirements for dockerization
```

## Data Transfer

This phase receives the data and process it with a hash before storing in an Elastic index
and MongoDB collection. It utilises Mongo and Elastic services and a hasher service to in order to properly send

### Build:
```bach
├── data_transfer
│ ├── Dockerfile - Containerizes application
│ ├── elastic_service.py - Elastic Service that uses CRUD model create and update
│ ├── hasher.py - Hashes files based on file paths
│ ├── kafka_reciever.py - Kafka consumer that recieves the data before passing it along
│ ├── main.py - Runs the program
│ ├── mongo_service.py - Mongo Service that uses CRUD model create and update
│ └── requirements.txt - Holds requirements for dockerization
```
## Utils:

This holds the Logger given in the side mission that sends to Elastic as well as displays on screen messages
alongside the config file which holds the proper environment structure for the applications using os.

### Build:
```bach

└── utils 
    ├── config.py - Holds env structure
    ├── logger.py - Tool to log events (uses: error, info)
    ├── decoder.py - Decodes encoded strings
    ├── load_data.py - Loads data from folder
    └── text_file_manager.py - Manages communication with text files
```

# Full build:

```bach
.
├── README.md
├── commands.bat
├── data
│ ├── negative_keywords.txt
│ ├── negative_keywords_encoded.txt
│ ├── neutral_keywords.txt
│ └── neutral_keywords_encoded.txt
├── data_ingestion
│ ├── Dockerfile
│ ├── kafka_sender.py
│ ├── main.py
│ ├── processor.py
│ └── requirements.txt
├── data_transfer
│ ├── Dockerfile
│ ├── elastic_service.py
│ ├── hasher.py
│ ├── kafka_reciever.py
│ ├── main.py
│ ├── mongo_service.py
│ └── requirements.txt
├── docker-compose.yaml
└── utils
    ├── config.py
    ├── decoder.py
    ├── load_data.py
    ├── logger.py
    ├── test.py
    └── text_file_manager.py
```
