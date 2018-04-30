import unittest

from src.ai import Ai
from src.board import Board
from src.coord import Coord
from src.trie import Trie

class TestAi(unittest.TestCase):

    def test_make_play(self):
        b = Board(3)
        b.place(("b", "u", "g"), Coord(1, 0), False)

        tiles = ["a", "e", "i", "o", "u", "y"]
        ai = Ai(tiles)

        trie = Trie.words()

        successful_play = ai.make_play(trie, b)
        self.assertTrue(successful_play)

    # tests that make_play doesn't work when the board is impossible
    def test_make_play_fail(self):
        b = Board(3)
        b.place(["b", "u", "g"], Coord(0, 0), True)
        b.place(["a", "g", "o"], Coord(0, 1), True)
        b.place(["a", "g"], Coord(0, 2), True)
        # this next line breaks crosschecks:
        # b.place(["x", "x"], Coord(0, 2), True)

        tiles = ["e", "i", "u", "y"]
        ai = Ai(tiles)
        trie = Trie.words()

        successful_play = ai.make_play(trie, b)
        self.assertFalse(successful_play)

    def test_remove_tiles(self):
        b = Board(3)
        b.place(("b", "u", "g"), Coord(1, 0), False)

        tiles = ["a", "e", "i", "o", "u", "y"]
        ai = Ai(tiles)

        trie = Trie.words()

        successful_play = ai.make_play(trie, b)
        self.assertNotEqual(len(ai.tiles), 7)
