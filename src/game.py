from src.ai import Ai
from src.bag import Bag
from src.board import Board
from src.trie import Trie

import time, random

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
        self.cur_player = self.player1
        self.skipped_turns = 0

    def play(self):
        while True:
            self.play_one_move()
            self.board.print_b()
            print(self.cur_player.tiles)
            print(self.cur_player.recent_score)
            print("----------")
            if self.skipped_turns > 5 or not self.cur_player.tiles:
                break
            time.sleep(3)

    def play_one_move(self):
        self.cur_player = self.player1 if self.cur_player == self.player2 else self.player2
        successful_play = self.cur_player.make_play(self.trie, self.board)
        if not successful_play:
            self.exchange_tiles()
            self.skipped_turns += 1
        else:
            self.replenish_tiles(self.cur_player)
            self.skipped_turns = 0

    def replenish_tiles(self, player):
        to_replen = 7 - len(player.tiles)
        while self.bag.has_tiles() and to_replen > 0:
            new_tile = self.bag.draw_tile()
            player.tiles.append(new_tile)
            to_replen -= 1

    def exchange_tiles(self):
        to_exchange = random.randrange(1, len(self.cur_player.tiles))
        exchange_list = []
        while self.bag.has_tiles() and to_exchange > 0:
            to_remove = choice(self.cur_player.tiles)
            self.cur_player.tiles.remove(to_remove)
            exchange_list.append(to_remove)

            new_tile = self.bag.draw_tile()
            self.cur_player.tiles.append(new_tile)
            to_exchange -= 1
        for t in exchange_list:
            self.bag.add_tile(t)
