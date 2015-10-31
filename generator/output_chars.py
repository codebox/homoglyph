from output_builder import OutputBuilder

class OutputChars(OutputBuilder):
    def __init__(self, output_dir, template_dir):
        self.file_name = 'chars.txt'
        OutputBuilder.__init__(self, output_dir, template_dir)

    def create(self, char_manager):
        template_text = self._get_template_text()

        lines = [template_text]
        for s in char_manager.get_list_of_sets():
            lines.append(''.join(s))
        self._write_output('\n'.join(lines))