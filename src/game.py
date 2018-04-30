from src.ai import Ai
from src.bag import Bag
from src.board import Board
from src.trie import Trie

# to think about:
# - check if player runs out of tiles and there are no more in bag. if so, quit.

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
        players = [self.player1, self.player2]
        i = 0
        while True:
            cur_player = players[i]
            successful_play = cur_player.make_play(self.board)
            if not successful_play:
                # in future: try to make exchange,
                # then break if unsuccessful
                break
            i = 1 if i == 0 else 0
            # pause!

    def end(self):
        pass
