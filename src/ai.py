import random, string
from src.start_seq import StartSequence
from src.coord import Coord

class Ai:
    def __init__(self, name, tiles):
        self.name = name
        self.tiles = tiles
        self.score = 0
        self.recent_score = 0

    def make_play(self, trie, board):
        # get starts
        starts = board.get_starts(len(self.tiles))

        possible_plays = []
        for start in starts:
            dist = start.points
            plays = trie.get_plays_constrained(start, self.tiles, board, dist)
            possible_plays.extend(plays)

        if not possible_plays:
            return False

        # place optimal word (or random at first)
        optimal_play = max(possible_plays)
        board.place(optimal_play.template,
            Coord(optimal_play.x, optimal_play.y), optimal_play.ish)

        self.remove_tiles(optimal_play.template)
        self.recent_score = optimal_play.points
        return optimal_play

    def remove_tiles(self, template):
        for l in template:
            if l:
                self.tiles.remove(l)
