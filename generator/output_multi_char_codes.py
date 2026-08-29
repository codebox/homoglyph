from output_builder import OutputBuilder

class OutputMultiCharCodes(OutputBuilder):
    """
    Writes raw_data/multi_char_codes.txt - the machine-readable list of multi-codepoint
    confusable mappings. Each line maps a single glyph to a prototype sequence:

        <glyph hex>;<space separated prototype hex codes>

    for example:

        fb03;66 66 69      # 'ﬃ' resembles "ffi"

    Only mappings whose prototype sequence is composed entirely of the given word characters
    are emitted - a prototype containing e.g. a combining mark can never appear in a searchable
    target word, so it would only ever add noise. This is the same alphabet used to filter the
    single-codepoint JavaScript map.
    """
    def __init__(self, output_dir, template_dir):
        self.file_name = 'multi_char_codes.txt'
        OutputBuilder.__init__(self, output_dir, template_dir)

    def create(self, multi_char_manager, chars):
        template_text = self._get_template_text()
        allowed = set(chars)

        lines = []
        for glyph, prototypes in multi_char_manager.get_list_of_mappings():
            glyph_code = self._hex_code_for_char(glyph)
            for prototype in prototypes:
                if not all(c in allowed for c in prototype):
                    continue
                prototype_codes = ' '.join(self._hex_code_for_char(c) for c in prototype)
                lines.append('{};{}'.format(glyph_code, prototype_codes))

        self._write_output('\n'.join([template_text] + lines))
