import random, string

class Ai:
    def __init__(self, tiles):
        self.tiles = []
        self.score = 0

    def make_play(self, board):
        # get starts
        board.get_starts(len(tiles))

        words = []
        for start in starts:
            words.extend(trie.get_words_constrained(self.tiles, board))
        if not words:
            return False
        # place optimal word (or random at first)
        # take out and replenish tiles
        # return True after successful play or exchange
        return True

        # return False to skip turn.
