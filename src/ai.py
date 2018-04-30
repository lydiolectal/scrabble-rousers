import random, string
from src.start_seq import StartSequence

class Ai:
    def __init__(self, tiles):
        self.tiles = tiles
        self.score = 0

    def make_play(self, trie, board):
        # get starts
        starts = board.get_starts(len(self.tiles))
        possible_plays = []
        for start in starts:
            possible_plays.extend(trie.get_words_constrained(start, self.tiles, board))

        if not possible_plays:
            return False
        # place optimal word (or random at first)
        # take out and replenish tiles
        # return True after successful play or exchange
        return True
