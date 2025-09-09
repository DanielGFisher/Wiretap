class TextFileManager:
    def __init__(self, filename):
        self.filename = filename

    def write_string_to_file(self, content_string):
        """
        Creates a text file and writes the given string content to it.
        If the file already exists, its content will be overwritten.
        :param content_string: String holding content to transfer to file
        """
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                file.write(content_string)
            print(f"Content successfully written to '{self.filename}'")
        except IOError as e:
            print(f"Error writing to file '{self.filename}': {e}")