from src.ai import Ai
from src.bag import Bag
from src.board import Board
from src.trie import Trie

import time

# to think about:
# - check if player runs out of tiles and there are no more in bag. if so, quit.

class Game:

    def __init__(self):
        self.bag = Bag()
        self.board = Board()
        self.trie = Trie.words()

        tiles1, tiles2 = [], []
        for _ in range(7):
            tiles1.append(self.bag.draw_tile())
            tiles2.append(self.bag.draw_tile())
        self.player1 = Ai(tiles1)
        self.player2 = Ai(tiles2)

    def play(self):
        players = [self.player1, self.player2]
        i = 0
        while True:
            cur_player = players[i]
            successful_play = cur_player.make_play(self.trie, self.board)
            if not successful_play:
                break
                return
            self.replenish_tiles(cur_player)
            i = 1 if i == 0 else 0
            self.board.print_b()
            print(cur_player.tiles)
            # pause!
            time.sleep(3)

    def replenish_tiles(self, player):
        to_replen = 7 - len(player.tiles)
        while self.bag.has_tiles() and to_replen > 0:
            new_tile = self.bag.draw_tile()
            player.tiles.append(new_tile)
            to_replen -= 1
