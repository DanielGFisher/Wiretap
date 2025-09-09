import hashlib
from utils.logger import Logger


class Hasher:
    def __init__(self, hash_algorithm=None):
        self.hasher = hashlib.new(hash_algorithm if hash_algorithm else 'md5')
        self.logger = Logger.get_logger()

    def generate_file_hash(self, file_path, chunk_size=8192):
        """
        Generates a hash for a file based on the file_path
        :param file_path: Path of the file to be hashed
        :param chunk_size: Size of file (8kb in this case)
        :return: File hash
        """
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                self.hasher.update(chunk)
        self.logger.info(f"Hash generated for {file_path} WAV file")
        return self.hasher.hexdigest()


# Test Usage
if __name__ == "__main__":
    h = Hasher()
    hash = h.generate_file_hash(r"C:\\Users\\danie\\Downloads\\podcasts-20250907T074751Z-1-001\\podcasts\\download.wav")
    print(hash)