import hashlib
from utils.logger import Logger


class Hasher:
    def __init__(self, hash_algorithm='md5'):
        self.hash_algorithm = hash_algorithm
        self.logger = Logger.get_logger()

    def generate_file_hash(self, file_path, chunk_size=8192):
        """
        Generates a hash for a file based on the file_path
        :param file_path: Path of the file to be hashed
        :param chunk_size: Size of file (8kb in this case)
        :return: File hash or None if error
        """
        hasher = hashlib.new(self.hash_algorithm)
        try:
            with open(file_path, 'rb') as f:
                while chunk := f.read(chunk_size):
                    hasher.update(chunk)
                    file_hash = hasher.hexdigest()
            self.logger.info(f"Hash generated for {file_path} WAV file")
            return file_hash
        except Exception as e:
            self.logger.error(f"Unable to hash due to error: {e}")
            return None


# Test Usage
if __name__ == "__main__":
    h = Hasher()
    hash = h.generate_file_hash(r"C:\\Users\\danie\\Downloads\\podcasts-20250907T074751Z-1-001\\podcasts\\download.wav")
    print(hash)