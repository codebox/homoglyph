from output_builder import OutputBuilder

class OutputCharCodes(OutputBuilder):
    def __init__(self, output_dir, template_dir):
        self.file_name = 'char_codes.txt'
        OutputBuilder.__init__(self, output_dir, template_dir)

    def create(self, char_manager):
        template_text = self._get_template_text()

        lines = []
        for s in char_manager.get_list_of_sets():
            codes = map(self._hex_code_for_char, s)
            lines.append(','.join(codes))
        self._write_output('\n'.join([template_text] + lines))