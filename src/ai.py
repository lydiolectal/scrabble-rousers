import random, string

class Ai:
    def __init__(self, board, trie):
        # self.tiles = [random.choice(string.ascii_lowercase) for _ in range(7)]
        self.tiles = ["c", "a", "s", "u", "k", "m", "p", "e", "d", "r", "s",
        "i", "t", "o"]
        self.board = board
        self.trie = trie

    def make_move(self):
        pass

    def exchange(self):
        pass
