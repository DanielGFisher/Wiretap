import json
from pathlib import Path
import wave
import speech_recognition as sr
from data_ingestion.load_data import DataLoader


class Processor:
    def __init__(self):
        self.data = []
        self.recognizer = sr.Recognizer()


    def get_text_from_wav(self,path):
        """
        Extract the text from the WAV file
        :param path: path to WAV file
        :return: Text from WAV file
        """
        with sr.AudioFile(path) as source:
            audio_data = self.recognizer.record(source)

            try:
                text = self.recognizer.recognize_google(audio_data)
                return text
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")


    def get_wav_creation_date(self, path):
        """
        Extracts the date of creation from WAV file
        :param path:
        :return:
        """
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
                    "metadata" : {
                        "text" : self.get_text_from_wav(str(file_path)),
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

    def create_json_object(self, files: list):
        """
        Creates a single JSON object to send with all the necessary data
        :return: JSON object full of Audio file links and metadata
        """

        obj = {}
        for i, file in range(len(files)):
            obj[f"file_{i}"] = self.get_metadata(file)


        data = json.dumps(obj, indent=4)

        return data


# Test Usage
if __name__ == "__main__":
    dl = DataLoader()

    p = Processor(dl.wav_files)

    wav_file = Path(r"C:\Users\danie\Downloads\podcasts-20250907T074751Z-1-001\podcasts\download.wav")
    metadata = p.get_metadata(wav_file)

    if metadata:
        for key, value in metadata.items():
            print(f"{key}: {value}")

    print(p.data)