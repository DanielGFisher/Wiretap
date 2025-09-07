import json
from operator import index
from pathlib import Path
import wave
from data_ingestion.load_data import DataLoader


class Processor:
    def __init__(self, link_list):
        self.data = self.create_json_object(link_list)

    def get_metadata(self, file_path: Path):
        """
        Extracts metadata from WAV files
        :param file_path: A Path object from pathlib that points to the WAV file
        :return: Python dictionary containing metadata or none if error occurs
        """
        if not file_path.is_file() or file_path.suffix.lower() != '.wav':
            print(f"Error: {file_path} is not a valid WAV file")
            return None

        try:
            with wave.open(str(file_path), 'rb') as wf:
                metadata = {
                    "direct_link" : str(file_path),
                    "metadata" : {
                        "nchannels": wf.getnchannels(),
                        "sampwidth": wf.getsampwidth(),
                        "framerate": wf.getframerate(),
                        "nframes": wf.getnframes(),
                        "comptype": wf.getcomptype(),
                        "compname": wf.getcompname(),
                        "duration_seconds": wf.getnframes() / wf.getframerate() if wf.getframerate() > 0 else 0
                    }
                }
                return metadata

        except wave.Error as e:
            print(f"Error reading WAV file {file_path}: {e}")
            return None

    def create_json_object(self, list: dict):
        """
        Creates a single JSON object to send with all the necessary data
        :return: JSON object full of Audio file links and metadata
        """
        object = {}
        for i in range(len(list)):
            object[f"file_{i}"] = self.get_metadata(list[i])


        data = json.dumps(object, indent=4)

        return data


if __name__ == "__main__":
    dl = DataLoader()

    p = Processor(dl.wav_files)

    wav_file = Path(r"C:\Users\danie\Downloads\podcasts-20250907T074751Z-1-001\podcasts\download.wav")
    metadata = p.get_metadata(wav_file)

    if metadata:
        for key, value in metadata.items():
            print(f"{key}: {value}")



    print(p.data)