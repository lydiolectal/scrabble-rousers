from src.ai import Ai
from src.bag import Bag
from src.board import Board
from src.trie import Trie

class Game:

    def __init__(self):
        self.bag = Bag()
        self.board = Board()
        self.trie = Trie()

        tiles1, tiles2 = [], []
        for _ in range(7):
            tiles1.append(bag.draw_tile())
            tiles2.append(bag.draw_tile())
        self.player1 = Ai(tiles1)
        self.player2 = Ai(tiles2)

    def play(self):
        pass

    def end(self):
        pass
