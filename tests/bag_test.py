import unittest

from src.bag import Bag

class TestBoard(unittest.TestCase):

    def test_draw_tile(self):
        b = Bag()
        # check that removing 8 items results in 90 remaining tiles
        for _ in range(8):
            b.draw_tile()
        num_remaining = sum(v for k, v in b.tiles.items())
        self.assertEqual(num_remaining, 90)

    def test_exchange(self):
        b = Bag()
        num_tiles = sum(v for k, v in b.tiles.items())
        self.assertEqual(num_tiles, 98)

        tiles = ["a", "b", "c"]
        for t in tiles:
            b.exchange_tile(t)

        num_remaining = sum(v for k, v in b.tiles.items())
        self.assertEqual(num_remaining, 98)
