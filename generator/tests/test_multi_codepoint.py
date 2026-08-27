import os
import sys
import tempfile
import unittest

# Allow the generator modules (which use flat imports) to be imported from the tests directory.
GENERATOR_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, GENERATOR_DIR)

from data_file_parser import DataFileLine, DataFileParser
from char_manager import CharacterManager
from multi_char_manager import MultiCharManager
from output_multi_char_codes import OutputMultiCharCodes


# A few real UTS #39 confusables.txt lines (single- and multi-codepoint targets).
SINGLE_LINE = '05AD ;\t0596 ;\tMA\t# ( x -> y )'
FFI_LINE    = 'FB03 ;\t0066 0066 0069 ;\tMA\t# ( ffi ligature )'
AE_LINE     = '00E6 ;\t0061 0065 ;\tMA\t# ( ae )'
M_LINE      = '006D ;\t0072 006E ;\tMA\t# ( m -> rn )'
COMMENT     = '# this is a comment'


class DataFileLineTest(unittest.TestCase):
    def test_single_codepoint_target_is_not_multi(self):
        line = DataFileLine(SINGLE_LINE)
        self.assertTrue(line.has_data())
        self.assertFalse(line.is_multi())
        self.assertEqual((chr(0x05AD), chr(0x0596)), line.get_chars())

    def test_multi_codepoint_target_is_multi(self):
        line = DataFileLine(FFI_LINE)
        self.assertTrue(line.has_data())
        self.assertTrue(line.is_multi())
        source, prototype = line.get_multi()
        self.assertEqual(chr(0xFB03), source)
        self.assertEqual('ffi', prototype)

    def test_multi_codepoint_two_char_prototype(self):
        source, prototype = DataFileLine(M_LINE).get_multi()
        self.assertEqual('m', source)
        self.assertEqual('rn', prototype)

    def test_comment_has_no_data(self):
        self.assertFalse(DataFileLine(COMMENT).has_data())


class DataFileParserTest(unittest.TestCase):
    def _parse(self, lines):
        with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write('\n'.join(lines))
            path = f.name
        try:
            return DataFileParser(path).parse()
        finally:
            os.remove(path)

    def test_parse_separates_single_and_multi(self):
        pairs, multi = self._parse([COMMENT, SINGLE_LINE, FFI_LINE, AE_LINE])
        self.assertEqual([(chr(0x05AD), chr(0x0596))], pairs)
        self.assertEqual({(chr(0xFB03), 'ffi'), ('æ', 'ae')}, set(multi))

    def test_multi_lines_are_no_longer_silently_dropped(self):
        # Regression: multi-codepoint targets used to raise in the old single-only parser
        # and were swallowed, so none of them reached the output.
        pairs, multi = self._parse([FFI_LINE, M_LINE])
        self.assertEqual([], pairs)
        self.assertEqual(2, len(multi))


class MultiCharManagerTest(unittest.TestCase):
    def test_add_and_lookup(self):
        m = MultiCharManager()
        m.add(chr(0xFB03), 'ffi')
        m.add('m', 'rn')
        self.assertEqual(['ffi'], m.get_prototypes_for_glyph(chr(0xFB03)))
        self.assertEqual(['rn'], m.get_prototypes_for_glyph('m'))
        self.assertEqual([], m.get_prototypes_for_glyph('z'))

    def test_deduplicates_prototypes(self):
        m = MultiCharManager()
        m.add(chr(0xFB03), 'ffi')
        m.add(chr(0xFB03), 'ffi')
        self.assertEqual(['ffi'], m.get_prototypes_for_glyph(chr(0xFB03)))

    def test_ignores_self_prototype(self):
        m = MultiCharManager()
        m.add('x', 'x')
        self.assertEqual([], m.get_prototypes_for_glyph('x'))

    def test_mappings_are_sorted(self):
        m = MultiCharManager()
        m.add('m', 'rn')
        m.add(chr(0xFB03), 'ffi')
        m.add('æ', 'ae')
        glyphs = [glyph for glyph, _ in m.get_list_of_mappings()]
        self.assertEqual(sorted(glyphs), glyphs)


class OutputMultiCharCodesTest(unittest.TestCase):
    def test_output_format(self):
        m = MultiCharManager()
        m.add(chr(0xFB03), 'ffi')
        m.add('m', 'rn')

        out_dir = tempfile.mkdtemp()
        template_dir = os.path.join(GENERATOR_DIR, 'templates')
        OutputMultiCharCodes(out_dir, template_dir).create(m, 'abcdefghijklmnopqrstuvwxyzfi')

        with open(os.path.join(out_dir, 'multi_char_codes.txt'), encoding='utf-8') as f:
            content = f.read()

        self.assertIn('fb03;66 66 69', content)
        self.assertIn('6d;72 6e', content)

    def test_output_excludes_prototypes_outside_alphabet(self):
        m = MultiCharManager()
        m.add(chr(0xFB03), 'ffi')
        m.add(chr(0x2A29), '-̓')  # prototype contains a combining mark

        out_dir = tempfile.mkdtemp()
        template_dir = os.path.join(GENERATOR_DIR, 'templates')
        OutputMultiCharCodes(out_dir, template_dir).create(m, 'abcdefghijklmnopqrstuvwxyz-.')

        with open(os.path.join(out_dir, 'multi_char_codes.txt'), encoding='utf-8') as f:
            content = f.read()

        self.assertIn('fb03;66 66 69', content)
        self.assertNotIn('2a29', content)


class GeneratedDataIntegrationTest(unittest.TestCase):
    """Checks the committed raw_data/multi_char_codes.txt actually contains real mappings."""
    def test_known_mappings_present(self):
        path = os.path.join(os.path.dirname(GENERATOR_DIR), 'raw_data', 'multi_char_codes.txt')
        with open(path, encoding='utf-8') as f:
            content = f.read()
        for expected in ('fb03;66 66 69', 'e6;61 65', '6d;72 6e', '153;6f 65'):
            self.assertIn(expected, content, '{} missing from generated data'.format(expected))


if __name__ == '__main__':
    unittest.main()
