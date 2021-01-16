#!python3

import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.joinpath('src')))
import texbrik

testdoc = Path(__file__).resolve().parent.joinpath('input_files/testinput1.brik')
tb = texbrik.brikFromDoc(testdoc)

class TestTexBrik(unittest.TestCase):

    def test_name(self):
        self.assertEqual(tb.name, 'testinput1')

    def test_prerequs(self):
        self.assertEqual(tb.prerequisites, [('testinput2', 't2')])

    def test_includes(self):
        self.assertEqual(tb.includes, ['amsmath', 'amssymb'])

    def test_content(self):
        self.assertTrue(tb.content)

if __name__ == '__main__':
    unittest.main()

