import unittest

from src.ai import Ai
from src.board import Board
from src.coord import Coord
from src.crosscheck_square import CrosscheckSquare
from src.start_seq import StartSequence
from src.trie import TrieNode

class TestAi(unittest.TestCase):

    def test_place_word(self):
        word_template = [c for c in "cabr"] + [None] + [c for c in "iole"]
        startCoord = Coord(3, 7)
        board = Board()
        board.place_word(word_template, startCoord, True)
        self.assertEqual(board.tiles[7][7], None)

    def test_getwords(self):
        trieRoot = TrieNode.words()

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
        actual = trieRoot.get_words_tiles(template, trieRoot, player.tiles)

        self.assertEqual(sorted(actual), sorted(expected))
        self.assertEqual(len(expected), len(actual))

        actual = trieRoot.get_words(template, trieRoot)
        self.assertEqual(sorted(actual), sorted(expected))
        self.assertEqual(len(expected), len(actual))

    def test_crosscheck(self):
        trieRoot = TrieNode.words()

        board = Board()
        testCoord = Coord(4, 8)
        # should be empty set
        expected = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
            'x', 'y', 'z'}
        self.assertEqual(board.get_v_check(testCoord), expected)

        startWord = "cabriole"
        startCoord = Coord(3, 7)
        board.place_word(startWord, startCoord, True)
        board.update_state(startCoord, len(startWord), True)
        # after placing "cabriole" at (7,3), v crosscheck for (8, 4) should be:
        expected = {'i', 's', 'e', 'w', 'g', 'm', 'n', 'l', 'd', 'a', 'y', 'x',
                    't', 'h', 'r'}
        self.assertEqual(board.get_v_check(testCoord), expected)

        board = Board()
        board.place_word(startWord, Coord(7, 3), False)
        board.update_state(Coord(7, 3), len(startWord), False)
        self.assertEqual(board.get_h_check(Coord(8, 4)), expected)

    def test_getchar(self):
        trieRoot = TrieNode.words()

        template = ["c", "a", "b", None, "i", "o", "l", "e"]
        self.assertEqual(trieRoot.get_chars(template, trieRoot), ["r"])
        template = ["c", "a", None]
        # print(trieRoot.get_chars(template, trieRoot))

    def test_update_neighbors(self):

        trieRoot = TrieNode.words()

        board = Board()
        testCoord = Coord(4, 8)
        startWord = "cabriole"
        startCoord = Coord(3, 7)
        board.place_word(startWord, startCoord, True)
        board.update_state(startCoord, len(startWord), True)
        # not a neighbor
        self.assertEqual(board.neighbors[9][4], False)
        # occupied
        self.assertEqual(board.neighbors[7][6], False)
        # should be neighbors
        self.assertEqual(board.neighbors[7][2], True)
        self.assertEqual(board.neighbors[6][9], True)
        self.assertEqual(board.neighbors[8][9], True)
        self.assertEqual(board.neighbors[7][11], True)

        starts = board.get_starts(5)
        # for start in starts:
        #     print(f"({start.x}, {start.y}): {start.template}")

        tiles = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

        start = StartSequence(4, 6, [None, "a", None, None, None, None, None, None, None], False)
        plays = trieRoot.get_words_constrained(start, trieRoot, tiles, board)
        # print("Times called: ", times_called)
        # print("Number of words: ", len(plays))
        # print(plays)

    # test that board gets proper start positions
    def test_get_starts(self):
        from collections import Counter

        b1 = Board(1)
        starts = b1.get_starts(1)
        self.assertEqual(len(starts), 2)
        start_coors = {(0,0)}
        self.assertEqual(start_coors, {(s.x, s.y) for s in starts})

        self.assertRaises(RuntimeError, lambda: Board(2))

        b2 = Board(3)
        starts = b2.get_starts(2)
        self.assertEqual(len(starts), 4)
        start_coors = {(1,1), (0,1), (1,0)}
        self.assertEqual(start_coors, {(s.x, s.y) for s in starts})
        c = Counter(s.ish for s in starts)
        self.assertEqual(c[True], 2)
        self.assertEqual(c[False], 2)

    def test_get_start_occupied(self):
        b3 = Board(5)
        b3.place(["a", "a"], Coord(1, 2), True)
        starts = b3.get_starts(2)

        def is_horizontal(start):
            return start.x == 1 and start.y == 2 and start.ish
        def is_vertical(start):
            return start.x == 1 and start.y == 2 and not start.ish
        self.assertEqual(len(list(filter(is_horizontal, starts))), 1)
        self.assertEqual(len(list(filter(is_vertical, starts))), 1)

        self.assertEqual(len(starts), 18)

    def test_update(self):
        b4 = Board(5)
        b4.place(["b", "u", "g"], Coord(2, 1), False)

        # neighbors
        self.assertEqual(b4.neighbors_set, {(1, 1), (1, 2), (1, 3), (2, 0),
                                            (2, 4), (3, 1), (3, 2), (3, 3)})
        self.assertFalse(b4.neighbors[1][2])
        self.assertTrue(b4.neighbors[2][3])

        # crosschecks
        self.assertEqual(b4.crosschecks[1][2].h_check, set())
        self.assertEqual(b4.crosschecks[1][3].h_check, {"a", "e", "i", "o", "y"})
