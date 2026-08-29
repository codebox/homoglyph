from output_builder import OutputBuilder

class OutputJS(OutputBuilder):
    def __init__(self, file_name, output_dir, template_dir):
        self.file_name = file_name
        OutputBuilder.__init__(self, output_dir, template_dir)

    def _make_map_for_required_chars(self, chars, char_manager):
        m = {}
        for char in chars:
            s = char_manager.get_set_for_char(char)
            # Sort by codepoint so the generated output is deterministic (independent
            # of Python's set iteration order / PYTHONHASHSEED) and regeneration is
            # byte-for-byte reproducible. Ordering does not affect behaviour because
            # lookups are membership tests.
            m[char] = sorted(filter(lambda c : c != char, s), key=ord)
        return m

    def _make_json_object_string(self, m):
        obj = [] # cant use json.dumps, rejects certain characters
        for k in sorted(m):
            s = []
            for x in m[k]:
                s.append('"\\u{' + '{:0>4}'.format(self._hex_code_for_char(x)) + '}"')
            obj.append('"{}": [{}]'.format(k, ', '.join(s)))
        return '{\n    ' + ',\n    '.join(obj) + '\n}'

    def _make_multi_map_for_required_chars(self, chars, multi_char_manager):
        # Only prototype sequences composed entirely of characters that a caller might
        # search for (the same alphabet used for the single-codepoint map) can ever match
        # a target word, so the runtime map is filtered down to those, keyed by glyph.
        allowed = set(chars)
        m = {}
        for glyph, prototypes in multi_char_manager.get_list_of_mappings():
            usable = [p for p in prototypes if all(c in allowed for c in p)]
            if usable:
                m[glyph] = usable
        return m

    def _make_multi_json_object_string(self, m):
        if not m:
            return '{}'
        obj = []
        for glyph in sorted(m):
            key = '"\\u{' + '{:0>4}'.format(self._hex_code_for_char(glyph)) + '}"'
            prototypes = []
            for prototype in m[glyph]:
                escaped = ''.join('\\u{' + '{:0>4}'.format(self._hex_code_for_char(c)) + '}' for c in prototype)
                prototypes.append('"' + escaped + '"')
            obj.append('{}: [{}]'.format(key, ', '.join(prototypes)))
        return '{\n    ' + ',\n    '.join(obj) + '\n}'

    def create(self, char_manager, chars, multi_char_manager):
        m = self._make_map_for_required_chars(chars, char_manager)
        json_str = self._make_json_object_string(m)

        multi_m = self._make_multi_map_for_required_chars(chars, multi_char_manager)
        multi_json_str = self._make_multi_json_object_string(multi_m)

        text = self._get_template_text() \
            .replace('[[chars_list]]', chars) \
            .replace('[[chars_json]]', json_str) \
            .replace('[[multi_chars_json]]', multi_json_str)

        self._write_output(text)
