import hashlib

class Hasher:
    def __init__(self, hash_algorithm=None):
        self.hasher = hashlib.new(hash_algorithm if hash_algorithm is not None else 'md5')

    def generate_file_hash(self, file_path, chunk_size=8192):
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                self.hasher.update(chunk)
        return self.hasher.hexdigest()


# Test Usage
if __name__ == "__main__":
    h = Hasher()
    hash = h.generate_file_hash(r"C:\\Users\\danie\\Downloads\\podcasts-20250907T074751Z-1-001\\podcasts\\download.wav")
    print(hash)