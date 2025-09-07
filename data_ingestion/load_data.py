from pathlib import Path
from data_ingestion.config import AUDIO_URL

class DataLoader:
    """
    Main function is to extract audio-files from a specified folder
    Args:
        folder_path (str): The path to the folder with the WAV files
    """
    def __init__(self, folder_path=None):
        self.folder_path = Path(AUDIO_URL) or Path(folder_path)
        self.wav_files = self.extract_wav_files()

    def extract_wav_files(self):
        """
        Retrieves a list of all files in the specified directory
        """
        wav_files = []
        for file_path in self.folder_path.glob("*.wav"):
            wav_files.append(file_path.resolve())
        return wav_files


# Test Usage
if __name__ == "__main__":
    dl = DataLoader()
    print(dl.wav_files)
