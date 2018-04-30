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

        b.print_b()
        print()
        successful_play = ai.make_play(trie, b)
        self.assertTrue(successful_play)
        b.print_b()

    # tests that make_play doesn't work when the board is impossible
    def test_make_play_fail(self):
        pass
