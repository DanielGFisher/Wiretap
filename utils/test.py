from utils.decoder import Decoder
from utils.text_file_manager import TextFileManager

if __name__ == "__main__":
    d = Decoder()
    tfm = TextFileManager()

    encoded = tfm.extract_from_txt_file("../data/negative_keywords_encoded.txt")

    decoded = d.decode_base64_string(encoded)

    tfm.write_list_to_file(decoded, "../data/negative_keywords.txt")

    encoded = tfm.extract_from_txt_file("../data/neutral_keywords_encoded.txt")

    decoded = d.decode_base64_string(encoded)

    tfm.write_list_to_file(decoded, "../data/neutral_keywords.txt")