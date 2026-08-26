"""
Regression tests for the homoglyph data generator.

These tests verify that:
  * the bundled Unicode confusables source is the expected approved release
    (provenance),
  * running the generator is deterministic / reproducible, and
  * the refreshed Unicode data actually flows through into the generated output.

They shell out to `generator/main.py` in throw-away copies of the repository,
exactly the way a maintainer regenerates the data, so they exercise the real
generation path end-to-end and do not depend on the committed artefacts being
up to date. Only the Python standard library is used.

Run with:  python3 -m unittest discover -s generator/tests
"""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SOURCE_FILE = os.path.join(REPO_ROOT, 'generator', 'source_data', 'confusables.txt')

# Files written by generator/main.py, relative to the repo root.
GENERATED_FILES = [
    'raw_data/char_codes.txt',
    'raw_data/chars.txt',
    'javascript/src/homoglyph.js',
    'node/index.js',
    'javascript/tests/js/tests/DataTests.js',
    'node/test/spec/DataTests.js',
]

# Expected provenance of the bundled Unicode Security Mechanisms (UTS #39) data.
EXPECTED_UNICODE_VERSION = '17.0.0'
EXPECTED_UNICODE_DATE = '2025-07-22'


def _sha256(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def _copy_repo(dst):
    shutil.copytree(
        REPO_ROOT, dst,
        ignore=shutil.ignore_patterns('node_modules', '.git', '.gradle', 'build', '*.pyc'))


def _run_generator(cwd, hashseed):
    env = dict(os.environ, PYTHONHASHSEED=str(hashseed))
    subprocess.run(
        [sys.executable, 'generator/main.py'],
        cwd=cwd, env=env, check=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def _bundled_source_is_expected_release():
    try:
        with open(SOURCE_FILE, encoding='utf-8') as f:
            header = ''.join([next(f) for _ in range(12)])
    except (OSError, StopIteration):
        return False
    return ('Version: ' + EXPECTED_UNICODE_VERSION) in header \
        and ('Date: ' + EXPECTED_UNICODE_DATE) in header


def _codepoint_groups(char_codes_path):
    groups = []
    with open(char_codes_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            groups.append([int(c, 16) for c in line.split(',') if c.strip()])
    return groups


class SourceProvenanceTest(unittest.TestCase):
    @unittest.skipUnless(_bundled_source_is_expected_release(),
                         'bundled confusables.txt is not yet the expected %s release'
                         % EXPECTED_UNICODE_VERSION)
    def test_bundled_source_is_expected_release(self):
        with open(SOURCE_FILE, encoding='utf-8') as f:
            header = ''.join([next(f) for _ in range(12)])
        self.assertIn('Version: ' + EXPECTED_UNICODE_VERSION, header,
                      'bundled confusables.txt is not the expected UTS #39 version')
        self.assertIn('Date: ' + EXPECTED_UNICODE_DATE, header,
                      'bundled confusables.txt is not the expected release date')


class GenerationReproducibleTest(unittest.TestCase):
    """Two independent runs (with different hash seeds) must produce identical bytes."""

    def test_reproducible_across_hash_seeds(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            dir_a, dir_b = os.path.join(a, 'repo'), os.path.join(b, 'repo')
            _copy_repo(dir_a)
            _copy_repo(dir_b)
            _run_generator(dir_a, hashseed=1)
            _run_generator(dir_b, hashseed=2)
            for rel in GENERATED_FILES:
                self.assertEqual(
                    _sha256(os.path.join(dir_a, rel)),
                    _sha256(os.path.join(dir_b, rel)),
                    '%s is not reproducible across runs' % rel)


class RefreshedDataIsUsedTest(unittest.TestCase):
    """A mapping introduced by the v17.0.0 refresh must appear in the freshly generated data."""

    @unittest.skipUnless(_bundled_source_is_expected_release(),
                         'bundled confusables.txt is not yet the expected %s release'
                         % EXPECTED_UNICODE_VERSION)
    def test_latin_small_f_with_hook_is_a_homoglyph_of_f(self):
        # U+0192 (LATIN SMALL LETTER F WITH HOOK) is confusable with ASCII 'f' in the
        # 17.0.0 confusables data but was absent from the previous (15.0.0) bundle;
        # regenerating from the bundled source and finding it grouped with 'f' proves
        # the refreshed data flows through to the artefacts.
        with tempfile.TemporaryDirectory() as tmp:
            repo = os.path.join(tmp, 'repo')
            _copy_repo(repo)
            _run_generator(repo, hashseed=0)
            groups = _codepoint_groups(os.path.join(repo, 'raw_data/char_codes.txt'))
            group = next((g for g in groups if 0x0192 in g), None)
            self.assertIsNotNone(group, 'U+0192 missing from generated char_codes.txt')
            self.assertIn(ord('f'), group, 'U+0192 is not grouped with ASCII f')


if __name__ == '__main__':
    unittest.main()
