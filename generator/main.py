from data_file_parser import DataFileDir
from char_manager import CharacterManager
from multi_char_manager import MultiCharManager
from output_char_codes import OutputCharCodes
from output_chars import OutputChars
from output_multi_char_codes import OutputMultiCharCodes
from output_js import OutputJS
from output_js_tests import OutputJSTests

TEMPLATES_DIR = 'generator/templates'
DATA_DIR      = 'generator/source_data'

CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-.'

if __name__ == '__main__':
    cm   = CharacterManager()
    mcm  = MultiCharManager()
    dfd  = DataFileDir(DATA_DIR)
    dfd.parse_all(cm, mcm)

    OutputCharCodes('raw_data', TEMPLATES_DIR).create(cm)
    OutputChars('raw_data', TEMPLATES_DIR).create(cm)
    OutputMultiCharCodes('raw_data', TEMPLATES_DIR).create(mcm, CHARS)
    OutputJS('homoglyph.js', 'javascript/src', TEMPLATES_DIR).create(cm, CHARS, mcm)
    OutputJS('index.js','node', TEMPLATES_DIR).create(cm, CHARS, mcm)
    OutputJSTests('DataTests.js','javascript/tests/js/tests', TEMPLATES_DIR).create(cm, CHARS)
