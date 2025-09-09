import json
import speech_recognition as sr
from datetime import datetime
from data_ingestion.load_data import DataLoader
from utils.logger import Logger

logger = Logger.get_logger()


class Processor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.logger = Logger.get_logger()

    def get_file_name(self, wav_file_path):
        """
        Extracts name from WAV file
        :param wav_file_path: Path to WAV file
        :return: Name of WAV file
        """
        try:
            file_name = wav_file_path.name
            logger.info(f"The name {file_name} was extracted from {wav_file_path}")
            return file_name
        except FileNotFoundError:
            logger.error(f"Error: File not found at '{wav_file_path}'")
        except Exception as e:
            logger.error(f"An error occurred: {e}")


    def get_text_from_wav(self,wav_file_path):
        """
        Extract the text from the WAV file
        :param wav_file_path: Path to WAV file
        :return: Text from WAV file
        """
        with sr.AudioFile(str(wav_file_path)) as source:
            audio_data = self.recognizer.record(source)

            try:
                text = self.recognizer.recognize_google(audio_data)
                logger.info(f"Text extracted from WAV file")
                return text
            except sr.UnknownValueError:
                logger.error("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                logger.error(f"Could not request results from Google Speech Recognition service; {e}")

    def get_file_size(self, wav_file_path):
        """
        Extract the size of WAV file
        :param wav_file_path: Path to WAV file
        :return: Size of WAV file
        """

        try:
            file_info = wav_file_path.stat()
            file_size_bytes = file_info.st_size
            logger.info(f"Extracted file size from {wav_file_path}")
            return file_size_bytes
        except FileNotFoundError:
            logger.error(f"Error: The file '{wav_file_path}' was not found.")
        except Exception as e:
            logger.error(f"An error occurred: {e}")


    def get_file_creation_date(self, wav_file_path):
        """
        Extracts the date of creation from WAV file
        :param wav_file_path: Path to WAV file
        :return: Date of creation
        """
        try:
            file_stats = wav_file_path.stat()
            creation_timestamp = file_stats.st_ctime
            creation_datetime = datetime.fromtimestamp(creation_timestamp)
            logger.info(f"Extracted date {creation_datetime} from {wav_file_path} WAV file")
            return creation_datetime
        except FileNotFoundError:
            logger.error(f"Error: File not found at '{wav_file_path}'")
        except Exception as e:
            logger.error(f"An error occurred: {e}")


    def create_json_object(self, file_path):
        """
        Creates a single JSON object to send with all the necessary data
        :return: JSON object full of Audio file links and metadata
        """

        data = {"wav_file_link": str(file_path),
                "metadata": {
                    "file_name": self.get_file_name(file_path),
                    "date_of_creation": str(self.get_file_creation_date(file_path)),
                    "size": self.get_file_size(file_path),
                    "text": self.get_text_from_wav(file_path)
                }
            }

        data = json.dumps(data, indent=4)
        logger.info(f"Extracted {data} from {file_path} WAV file")
        return data



# Test Usage
if __name__ == "__main__":
    dl = DataLoader()

    p = Processor()

    print(p.create_json_object(dl.wav_files[0]))
