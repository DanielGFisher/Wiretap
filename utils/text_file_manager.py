from utils.logger import Logger


class TextFileManager:
    def __init__(self):
        self.logger = Logger.get_logger()

    def write_list_to_file(self, content_string, file_name):
        """
        Creates a text file and writes the given string content to it.
        If the file already exists, its content will be overwritten.
        :param content_string: String holding content to transfer to file
        :param file_name: Name or path of the file
        """
        try:
            words = content_string.split(",")
            with open(file_name, 'w', encoding='utf-8') as file:
                for word in words:
                    file.write(word + '\n')
            self.logger.info(f"Content successfully written to '{file_name}'")
        except IOError as e:
            self.logger.error(f"Error writing to file '{file_name}': {e}")


    def extract_from_txt_file(self, path):
        """
        Extracts content from file
        :param path: Path to the file
        :return: content of the txt file
        """
        try:
            with open(path, "r") as f:
                content = f.read()
                return content
        except FileNotFoundError:
            self.logger.error(f"Error: The file {path} was not found.")
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")

# Test Usage
if __name__ == "__main__":
    tfm = TextFileManager()
    extracted = tfm.extract_from_txt_file("../data/negative_keywords_encoded.txt")

    print(type(extracted))