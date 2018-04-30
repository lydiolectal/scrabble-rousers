import unittest
from src.ai import Ai
from src.board import Board
from src.coord import Coord
from src.crosscheck_square import CrosscheckSquare
from src.start_seq import StartSequence
from src.trie import Trie

class TestTrie(unittest.TestCase):

    def test_contains(self):
        # insert a word into trie
        t = Trie()
        t.insert("abba")
        self.assertTrue(t.contains("abba"))
        self.assertFalse(t.contains("hen"))
        self.assertFalse(t.contains("ab"))

    def test_get_char(self):
        trieRoot = Trie.words()

        template = ["c", "a", "b", None, "i", "o", "l", "e"]
        self.assertEqual(trieRoot.get_chars(template), ["r"])
        template = ["c", "a", None]

        invalid_template = ["s", None, None, "e"]
        self.assertRaises(RuntimeError, lambda: trieRoot.get_chars(invalid_template))

    def test_get_words_constrained(self):
        trieRoot = Trie.words()

        board = Board()
        testCoord = Coord(4, 8)
        startWord = "cabriole"
        startCoord = Coord(3, 7)
        board.place(("c", "a", "b", "r", "i", "o", "l", "e"), startCoord, True)

        tiles = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

        start = StartSequence(4, 6, [None, "a", None, None, None, None,
            None, None, None], False)
        plays = trieRoot.get_words_constrained(start, tiles, board)
        plays = [tuple(play) for play in plays]

        self.assertEqual(set(plays), {('b', None), ('b', None, 'd'),
        ('b', None, 'd', 'e'), ('b', None, 'd', 'g', 'e'), ('b', None, 'a'),
        ('b', None, 'a', 'e', 'd'), ('b', None, 'g'), ('f', None),
        ('f', None, 'd'), ('f', None, 'd', 'e'), ('f', None, 'd', 'g', 'e'),
        ('f', None, 'c', 'e'), ('f', None, 'c', 'e', 'd'),
        ('f', None, 'c', 'a', 'd', 'e'), ('f', None, 'g'), ('d', None),
        ('d', None, 'b'), ('d', None, 'c', 'e'), ('d', None, 'g'), ('a', None),
        ('c', None, 'b'), ('c', None, 'f', 'e'), ('c', None, 'd'),
        ('c', None, 'd', 'e'), ('c', None, 'd', 'g', 'e'), ('c', None, 'g', 'e'),
        ('c', None, 'g', 'e', 'd'), ('g', None, 'b'), ('g', None, 'e'),
        ('g', None, 'e', 'd'), ('g', None, 'd')})

        board.place(plays[10], Coord(start.x, start.y), start.ish)

    def test_get_words_constrained_full(self):
        trieRoot = Trie.words()
        b4 = Board(3)
        b4.place(("b", "u", "g"), Coord(1, 0), False)

        starts = b4.get_starts(6)
        words = []
        tiles = ["a", "e", "i", "o", "u", "y"]

        for start in starts:
            words.extend(trieRoot.get_words_constrained(start, tiles, b4))
        words = [tuple(word) for word in words]

        self.assertEqual(set(words), {('a', None, 'o'), ('a', None, 'y'),
        ('o', None, 'e'), ('o', None, 'i'), (None, 'e'), (None, 'a'),
        (None, 'i'), (None, 'o'), (None, 'y'), (None, 'o'), ('e', None, 'o'),
        ('a', None), ('a', None, 'e'), ('a', None, 'o')})
