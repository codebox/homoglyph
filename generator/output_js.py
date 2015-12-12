from output_builder import OutputBuilder

class OutputJS(OutputBuilder):
    def __init__(self, file_name, output_dir, template_dir):
        self.file_name = file_name
        OutputBuilder.__init__(self, output_dir, template_dir)

    def _make_map_for_required_chars(self, chars, char_manager):
        m = {}
        for char in chars:
            s = char_manager.get_set_for_char(char)
            m[char] = list(filter(lambda c : c != char, s))
        return m

    def _make_json_object_string(self, m):
        obj = [] # cant use json.dumps, rejects certain characters
        for k in sorted(m):
            s = []
            for x in m[k]:
                s.append('"\\u{' + '{:0>4}'.format(self._hex_code_for_char(x)) + '}"')
            obj.append('"{}": [{}]'.format(k, ', '.join(s)))
        return '{\n    ' + ',\n    '.join(obj) + '\n}'

    def create(self, char_manager, chars):
        m = self._make_map_for_required_chars(chars, char_manager)
        json_str = self._make_json_object_string(m)

        text = self._get_template_text().replace('[[chars_list]]', chars).replace('[[chars_json]]', json_str)

        self._write_output(text)
