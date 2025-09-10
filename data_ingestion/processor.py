import json
import speech_recognition as sr
from datetime import datetime
from utils.config import NEUTRAL_WORDS, HOSTILE_WORDS
from utils.load_data import DataLoader
from utils.logger import Logger
from utils.text_file_manager import TextFileManager


class Processor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.logger = Logger.get_logger()
        self.tfm = TextFileManager()
        self.neutral_words = self.load_word_list(NEUTRAL_WORDS)
        self.hostile_words = self.load_word_list(HOSTILE_WORDS)

    def get_file_name(self, wav_file_path):
        """
        Extracts name from WAV file
        :param wav_file_path: Path to WAV file
        :return: Name of WAV file
        """
        try:
            file_name = wav_file_path.name
            self.logger.info(f"The name {file_name} was extracted from {wav_file_path}")
            return file_name
        except FileNotFoundError:
            self.logger.error(f"Error: File not found at '{wav_file_path}'")
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")

    def load_word_list(self, path):
        """
        Get a .txt file path and extract the words before putting
        them in a list
        :param path: .txt file path
        :return: List of strings from .txt file or empty list
        """
        if path:
            content = self.tfm.extract_from_txt_file(path)
            if content:
                return [w.strip().lower() for w in content.split("\n") if w.strip()]
            return []

    def analyse_bds(self, text):
        """
        Go through text and determine if it classifies as BDS
        (Boycott, Divest, Sanction) and provide ranking and
        sentiment rank keyword
        :param text: Text derived from WAV file
        :return: bds_percent - number rank of text
                 is_bds - text classifies as bds
                 bds_threat_level - keyword rank of text
        """

        text_lower = text.lower()
        total_words = len(text_lower.split()) or 1
        hostile_count = sum(text_lower.count(w) for w in self.neutral_words)
        neutral_count = sum(text_lower.count(w) for w in self.hostile_words)
        bds_percent = (hostile_count + neutral_count) / total_words * 100
        is_bds = bds_percent > 5
        if bds_percent <= 5:
            bds_threat_level = "None"
        elif 5 < bds_percent <= 10:
            bds_threat_level = "Neutral"
        else:
            bds_threat_level = "Hostile"

        return bds_percent, is_bds, bds_threat_level

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
                self.logger.info(f"Text extracted from WAV file")
                return text
            except sr.UnknownValueError:
                self.logger.error("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                self.logger.error(f"Could not request results from Google Speech Recognition service; {e}")

    def get_file_size(self, wav_file_path):
        """
        Extract the size of WAV file
        :param wav_file_path: Path to WAV file
        :return: Size of WAV file
        """

        try:
            file_info = wav_file_path.stat()
            file_size_bytes = file_info.st_size
            self.logger.info(f"Extracted file size from {wav_file_path}")
            return file_size_bytes
        except FileNotFoundError:
            self.logger.error(f"Error: The file '{wav_file_path}' was not found.")
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")


    def get_file_creation_date(self, wav_file_path):
        """
        Extracts the date of creation from WAV file
        :param wav_file_path: Path to WAV file
        :return: Date of creation
        """
        try:
            file_stats = wav_file_path.stat()
            creation_timestamp = file_stats.st_ctime
            creation_datetime = datetime.fromtimestamp(creation_timestamp).isoformat()
            self.logger.info(f"Extracted date {creation_datetime} from {wav_file_path} WAV file")
            return creation_datetime
        except FileNotFoundError:
            self.logger.error(f"Error: File not found at '{wav_file_path}'")
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")


    def create_json_object(self, file_path):
        """
        Creates a single JSON object to send with all the necessary data
        :return: JSON object full of Audio file links and metadata
        """
        content = self.get_text_from_wav(file_path)

        bds_percent, is_bds, bds_threat_level = self.analyse_bds(content)
        data = {
                "wav_file_link": str(file_path),
                    "metadata": {
                        "file_name": self.get_file_name(file_path),
                        "date_of_creation": self.get_file_creation_date(file_path),
                        "size": self.get_file_size(file_path),
                    },
                    "text": {
                        "content": content,
                        "bds_percent": bds_percent,
                        "is_bds": is_bds,
                        "bds_threat_level": bds_threat_level
                    }
                }

        data = json.dumps(data, indent=4)
        self.logger.info(f"Extracted {data} from {file_path} WAV file")
        return data



# Test Usage
if __name__ == "__main__":
    dl = DataLoader()

    p = Processor()

    print(p.create_json_object(dl.wav_files[0]))
