import unittest
from src.trie import Trie

class TestTrie(unittest.TestCase):

    def test_contains(self):
        # insert a word into trie
        t = Trie()
        t.insert("abba")
        self.assertTrue(t.contains("abba"))
        self.assertFalse(t.contains("hen"))
        self.assertFalse(t.contains("ab"))

    # def test_get_words(self):
    #     trieRoot = TrieNode.words()
    #     b4 = Board(5)
    #     b4.place(["b", "u", "g"], Coord(2, 1), False)
