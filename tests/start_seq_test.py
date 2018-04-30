import unittest
from src.start_seq import StartSequence

class TestStartSequence(unittest.TestCase):

    def test_eq(self):
        x = 0
        y = 0
        template = ["a"]
        ish = True

        s1 = StartSequence(x, y, template, ish, 1)
        s2 = StartSequence(x, y, template, ish, 1)
        self.assertTrue(s1 == s2)

        s3 = StartSequence(x, y, template, ish, 3)
        self.assertFalse(s3 == s2)

    def test_ne(self):
        x = 0
        y = 0
        template = ["a"]
        ish = True

        s1 = StartSequence(x, y, template, ish, 1)
        s2 = StartSequence(x, y, template, ish, 5)
        self.assertTrue(s1 != s2)

        s3 = StartSequence(x, y, template, ish, 5)
        self.assertFalse(s3 != s2)

    def test_le(self):
        x = 0
        y = 0
        template = ["a"]
        ish = True

        s1 = StartSequence(x, y, template, ish, 1)
        s2 = StartSequence(x, y, template, ish, 5)
        self.assertTrue(s1 < s2)
        self.assertTrue(s1 <= s2)
        self.assertFalse(s2 < s1)

    def test_ge(self):
        x = 0
        y = 0
        template = ["a"]
        ish = True

        s1 = StartSequence(x, y, template, ish, 1)
        s2 = StartSequence(x, y, template, ish, 5)
        self.assertTrue(s2 > s1)
        self.assertTrue(s2 >= s1)
        self.assertFalse(s1 > s2)

    def test_max(self):
        x = 0
        y = 0
        template = ["a"]
        ish = True
        s1 = StartSequence(x, y, template, ish, 1)
        s2 = StartSequence(x, 1, template, ish, 5)
        s3 = StartSequence(x, 2, template, ish, 5)

        larger = max(s1, s2)
        self.assertEqual(larger, s2)
