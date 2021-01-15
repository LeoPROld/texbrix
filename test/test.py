#!python3

import texbrik
import unittest

testdoc = "testinput.brik"
tb = texbrik.brikFromDoc(testdoc)

class TestTexBrik(unittest.TestCase):

    def test_name(self):
        self.assertEqual(tb.name, 'testinput1')

    def test_prerequs(self):
        self.assertEqual(tb.prerequisites, ['a', 'b'])

    def test_includes(self):
        self.assertEqual(tb.includes, ['amsmath', 'amssymb'])

    def test_content(self):
        self.assertTrue(tb.content)

if __name__ == '__main__':
    unittest.main()

