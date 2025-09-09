from pathlib import Path
from utils.config import AUDIO_URL
from utils.logger import Logger


class DataLoader:
    """
    Main function is to extract audio-files from a specified folder
    Args:
        folder_path (str): The path to the folder with the WAV files
    """
    def __init__(self, folder_path=None):
        self.folder_path = Path(folder_path) if folder_path else Path(AUDIO_URL)
        self.wav_files = self.extract_wav_files()
        self.logger = Logger.get_logger()


    def extract_wav_files(self):
        """
        Retrieves a list of all files in the specified directory
        """
        wav_files = []
        for file_path in self.folder_path.glob("*.wav"):
            wav_files.append(file_path.resolve())
            return wav_files


    def extract_from_txt_file(self, path):
        try:
            with open(path, "r") as file_object:
                content = file_object.read()
                print(content)
        except FileNotFoundError:
            self.logger.error(f"Error: The file {path} was not found.")
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")



# Test Usage
if __name__ == "__main__":
    dl = DataLoader()
    print(dl.wav_files)
    print()
    print(dl.extract_from_txt_file(r"C:\Users\danie\PycharmProjectsc\Wiretap\data\negative_keywords_encoded.txt"))