from output_builder import OutputBuilder

class OutputJSTests(OutputBuilder):
    def __init__(self, file_name, output_dir, template_dir):
        self.file_name = file_name
        OutputBuilder.__init__(self, output_dir, template_dir)

    def create(self, char_manager, chars):
        check_statements = []
        for char in chars:
            char_homoglyphs = char_manager.get_set_for_char(char)
            char_homoglyphs_as_unicode = []
            for char_homoglyph in char_homoglyphs:
                char_homoglyphs_as_unicode.append('"\\u{' + '{:0>4}'.format(self._hex_code_for_char(char_homoglyph)) + '}"')

            check_statements.append('    check("{}", [{}]);'.format(char, ' ,'.join(char_homoglyphs_as_unicode)))

        text = self._get_template_text().replace('[[check_statements]]', '\n'.join(check_statements))

        self._write_output(text)
