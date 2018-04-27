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

    def test_get_words(self):
        trieRoot = Trie.words()

        template = ["a", "b", "a", None, None, None]
        expected = []
        with open("assets/sample.txt") as f:
            for line in f.read().splitlines():
                if len(line) == 6:
                    expected.append(line)
        # we expect: ['abacas', 'abacus', 'abakas', 'abamps', 'abased',
        #'abaser', 'abases', 'abasia', 'abated', 'abater', 'abates',
        #'abatis', 'abator']

        player = Ai()
        actual = trieRoot.get_words_tiles(template, player.tiles)

        self.assertEqual(sorted(actual), sorted(expected))
        self.assertEqual(len(expected), len(actual))

        actual = trieRoot.get_words(template)
        self.assertEqual(sorted(actual), sorted(expected))
        self.assertEqual(len(expected), len(actual))

    def test_get_words_constrained(self):
        trieRoot = Trie.words()

        board = Board()
        testCoord = Coord(4, 8)
        startWord = "cabriole"
        startCoord = Coord(3, 7)
        board.place(["c", "a", "b", "r", "i", "o", "l", "e"], startCoord, True)

        tiles = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

        start = StartSequence(4, 6, [None, "a", None, None, None, None, None, None, None], False)
        plays = trieRoot.get_words_constrained(start, tiles, board)
        self.assertEqual(set(plays), {'cad', 'cade', 'cadge', 'cab', 'cafe', 'cage',
        'caged', 'da', 'dace', 'dab', 'dag', 'aa', 'ba', 'bad', 'bade', 'badge',
        'baa', 'baaed', 'bag', 'fa', 'face', 'faced', 'facade', 'fad', 'fade',
        'fadge', 'fag', 'gae', 'gaed', 'gad', 'gab'})

    def test_get_words(self):
        trieRoot = Trie.words()
        b4 = Board(3)
        b4.place(["b", "u", "g"], Coord(1, 0), False)

        starts = b4.get_starts(6)
        words = []
        tiles = ["a", "e", "i", "o", "u", "y"]

        for start in starts:
            words.extend(trieRoot.get_words_constrained(start, tiles, b4))

        self.assertEqual(set(words), {'obi', 'obe', 'abo', 'aby', 'bi', 'bo',
            'by', 'be', 'ba', 'go', 'ego', 'ag', 'ago', 'age'})
