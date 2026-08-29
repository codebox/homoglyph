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

    def _get_target_codes(self):
        return self.parts[1].strip().split()

    def is_multi(self):
        # A confusable whose target (prototype) is a sequence of more than one codepoint,
        # e.g. 'ﬃ' (U+FB03) is confusable with the sequence "ffi" (0066 0066 0069).
        return len(self._get_target_codes()) > 1

    def get_chars(self):
        # Single-codepoint mapping: (source char, target char)
        return self._get_char_from_code(self.parts[0]), self._get_char_from_code(self.parts[1])

    def get_multi(self):
        # Multi-codepoint mapping: (source char, target string)
        source = self._get_char_from_code(self.parts[0])
        target = ''.join(self._get_char_from_code(c) for c in self._get_target_codes())
        return source, target

class DataFileParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self):
        char_pairs = []
        multi_maps = []
        with open(self.file_path, encoding='utf-8') as f:
            for line_text in f:
                line = DataFileLine(line_text)
                if line.has_data():
                    try:
                        if line.is_multi():
                            multi_maps.append(line.get_multi())
                        else:
                            char_pairs.append(line.get_chars())
                    except:
                        pass

        return char_pairs, multi_maps

class DataFileDir:
    def __init__(self, dir_name):
        self.dir_name = dir_name

    def parse_all(self, char_manager, multi_char_manager=None):
        for file in sorted(os.listdir(self.dir_name)):
            char_pairs, multi_maps = DataFileParser(os.path.join(self.dir_name, file)).parse()
            for pair in char_pairs:
                char_manager.add_pair(*pair)
            if multi_char_manager is not None:
                for source, target in multi_maps:
                    multi_char_manager.add(source, target)
