import random, string
from src.start_seq import StartSequence
from src.coord import Coord

class Ai:
    def __init__(self, tiles):
        self.tiles = tiles
        self.score = 0

    def make_play(self, trie, board):
        # get starts
        starts = board.get_starts(len(self.tiles))
        possible_plays = []
        for start in starts:
            possible_plays.extend(trie.get_plays_constrained(start, self.tiles, board))

        if not possible_plays:
            return False
        # place optimal word (or random at first)
        optimal_play = max(possible_plays)
        board.place(optimal_play.template,
            Coord(optimal_play.x, optimal_play.y), optimal_play.ish)
        # TODO: take out and replenish tiles -- needs to be done by game
        # return True after successful play or exchange
        return True
