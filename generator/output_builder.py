import os.path

class OutputBuilder:
    def __init__(self, output_dir, template_dir):
        self.output_dir = output_dir
        self.template_dir = template_dir

    def _write_output(self, text):
        with open(os.path.join(self.output_dir, self.file_name), encoding='utf-8', mode='w') as f:
            f.write(text)

    def _get_template_text(self):
        with open(os.path.join(self.template_dir, self.file_name), encoding='utf-8') as f:
            return f.read()

    def _hex_code_for_char(self, c):
        return hex(ord(c))[2:]