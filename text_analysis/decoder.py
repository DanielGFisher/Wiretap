import base64
from utils.logger import Logger


class Decoder:
    def __init__(self):
        self.logger = Logger.get_logger()

    def decode_base64_string(self, encoded_string: str) -> str:
        """
        Decodes a Base64 encoded string
        :param encoded_string: The Base64 encoded string to decode
        :return : The decoded string
        """
        if not isinstance(encoded_string, str):
            raise TypeError("Input must be a string.")

        try:
            base64_bytes = encoded_string.encode("utf-8")
            decoded_bytes = base64.b64decode(base64_bytes)
            decoded_string = decoded_bytes.decode('utf-8')
            self.logger.info(f"Encoded message {encoded_string} decoded successfully!")
            return decoded_string
        except Exception as e:
            self.logger.error(f"Invalid Base64 string: {e}")
        except UnicodeDecodeError as e:
            self.logger.error(f"Error decoding bytes to string: {e}")

if __name__ == "__main__":
    decoder = Decoder()

    decoded = decoder.decode_base64_string("R2Vub2NpZGUsV2FyIENyaW1lcyxBcGFydGhpZCxNYXNzYWNyZSxOYWtiYSxEaXNwbGFjZW1lbnQsSHVtYW5pdGFyaWFuIENyaXNpcyxCbG9ja2FkZSxPY2N1cGF0aW9uLFJlZnVnZXVzLElDQyxCRFM=")

    print(decoded)