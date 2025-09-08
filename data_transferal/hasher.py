import hashlib
import json

class Processor:
    def __init__(self, data):
        self.data = data

    def generate_file_hash(self, file_path, hash_algorithm='md5', chunk_size=8192):
        hasher = hashlib.new(hash_algorithm)
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                hasher.update(data)
        self.data['ID'] = hasher.hexdigest()

    def split_records(self):
        data = json.loads(self.data)
        records = []
        for key, value in data.items():
            record = value
            record["file_key"] = key
            records.append(record)
        return records


# Test Usage
if __name__ == "__main__":
    p = Processor(
        {
        "file_33": {
            "direct_link": "C:\\Users\\danie\\Downloads\\podcasts-20250907T074751Z-1-001\\podcasts\\download.wav",
                "metadata":
                    {
                    "nchannels": 1,
                    "sampwidth": 2,
                    "framerate": 24000,
                    "nframes": 1165703,
                    "comptype": "NONE",
                    "compname": "not compressed",
                    "duration_seconds": 48.57095833333333
                }
            }
        }
    )
    p.split_records()
    p.generate_file_hash(r"C:\\Users\\danie\\Downloads\\podcasts-20250907T074751Z-1-001\\podcasts\\download.wav")

    print(p.data)