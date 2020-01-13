from data_file_parser import DataFileDir
from char_manager import CharacterManager
from output_char_codes import OutputCharCodes
from output_chars import OutputChars
from output_js import OutputJS
from output_js_tests import OutputJSTests

TEMPLATES_DIR = 'generator/templates'
DATA_DIR      = 'generator/source_data'

CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-.'

if __name__ == '__main__':
    cm  = CharacterManager()
    dfd = DataFileDir(DATA_DIR)
    dfd.parse_all(cm)

    OutputCharCodes('raw_data', TEMPLATES_DIR).create(cm)
    OutputChars('raw_data', TEMPLATES_DIR).create(cm)
    OutputJS('homoglyph.js', 'javascript/src', TEMPLATES_DIR).create(cm, CHARS)
    OutputJS('index.js','node', TEMPLATES_DIR).create(cm, CHARS)
    OutputJSTests('DataTests.js','javascript/tests/js/tests', TEMPLATES_DIR).create(cm, CHARS)
