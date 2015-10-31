import os
import os.path

class DataFileLine:
    def __init__(self, text):
        self.text = text.strip()
        self.parts = self.text.split(';', 2)

    def has_data(self):
        return (not self.text.startswith('#')) and len(self.parts) >= 2

    def _get_char_from_code(self, code):
        return chr(int(code.strip(), 16))

    def get_chars(self):
        return self._get_char_from_code(self.parts[0]), self._get_char_from_code(self.parts[1])

class DataFileParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self):
        char_pairs = []
        with open(self.file_path, encoding='utf-8') as f:
            for line_text in f:
                line = DataFileLine(line_text)
                if line.has_data():
                    try:
                        char_pairs.append(line.get_chars())
                    except:
                        pass

        return char_pairs

class DataFileDir:
    def __init__(self, dir_name):
        self.dir_name = dir_name

    def parse_all(self, char_manager):
        for file in os.listdir(self.dir_name):
            char_pairs = DataFileParser(os.path.join(self.dir_name, file)).parse()
            for pair in char_pairs:
                char_manager.add_pair(*pair)


