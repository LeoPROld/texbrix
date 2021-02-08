#!python3

from texbrix import texbrik
import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.joinpath('src')))

testdoc = Path(__file__).resolve().parent.joinpath(
    'input_files/testinput1.brik')


class TestTexBrik(unittest.TestCase):

    def test_packages(self):
        tb = texbrik.brikFromDoc(testdoc)
        self.assertEqual(set(['amssymb']), tb.packages)

    def test_content(self):
        tb = texbrik.brikFromDoc(testdoc)
        self.assertTrue(tb.content)

    def test_expand_brikinserts(self):
        tb = texbrik.brikFromDoc(testdoc)
        tb.expand()
        self.assertIn('testinput2', tb.brikinserts.keys())

    def test_expand_packages(self):
        tb = texbrik.brikFromDoc(testdoc)
        tb.expand()
        self.assertNotEqual([i for i in tb.packages if i != 'amssymb'], {})

    def test_expand_content(self):
        tb = texbrik.brikFromDoc(testdoc)
        tb.expand()
        self.assertNotEqual(tb.content.find('in3'), -1)


if __name__ == '__main__':
    unittest.main()
