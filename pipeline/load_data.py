import os
import wave
from pipeline.config import AUDIO_URL

class DataLoader:
    """
    Main function is to extract audio-files from a specified folder
    Args:
        folder_path (str): The path to the folder with the WAV files
    """
    def __init__(self, folder_path=None):
        self.folder_path = AUDIO_URL or folder_path
        self.wav_files = self.extract_wav_files()

    def extract_wav_files(self):
        """
        Retrieves a list of all files in the specified directory
        """
        files = []
        for entry in os.listdir(self.folder_path):
            full_path = os.path.join(self.folder_path, entry)
            if os.path.isfile(full_path):
                files.append(full_path)
        return files

if __name__ == "__main__":
    dl = DataLoader()
    print(dl.wav_files)
