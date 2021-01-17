#!python3

import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.joinpath('src')))
import texbrik

testdoc = Path(__file__).resolve().parent.joinpath('input_files/testinput1.brik')

class TestTexBrik(unittest.TestCase):

    def test_includes(self):
        tb = texbrik.brikFromDoc(testdoc, testdoc.parent)
        self.assertEqual(['amssymb'], tb.includes)

    def test_content(self):
        tb = texbrik.brikFromDoc(testdoc, testdoc.parent)
        self.assertTrue(tb.content)

    def test_expand_brikinserts(self):
        tb = texbrik.brikFromDoc(testdoc, testdoc.parent)
        tb.expand()
        self.assertIn('testinput2', tb.brikinserts.keys())

    def test_expand_includes(self):
        tb = texbrik.brikFromDoc(testdoc, testdoc.parent)
        tb.expand()
        self.assertNotEqual([i for i in tb.includes if i != 'amssymb'], {})

    def test_expand_content(self):
        tb = texbrik.brikFromDoc(testdoc, testdoc.parent)
        tb.expand()
        self.assertNotEqual(tb.content.find('in3'), -1)


if __name__ == '__main__':
    unittest.main()

