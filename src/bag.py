import random

# keeps track of tile bag, and allows players to draw and exchange tiles
class Bag:
    def __init__(self):
        # dictionary isn't really random; should be weighted based on tile freq
        self.tiles = {
        "e":12, "a":9, "i":9, "o":8, "n":6, "r":6, "t":6, "l":4, "s":4, "u":4,
        "d":4, "g":3, "b":2, "c":2, "m":2, "p":2, "f":2, "h":2, "v":2, "w":2,
        "y":2, "k":1, "j":1, "x":1, "q":1, "z":1}

    # return a letter from the Bag inventory, and delete
    # returns False if Bag is empty
    def draw_tile(self):
        if not(self.has_tiles()):
            return None
        else:
            tile_list = []
            for (k, v) in self.tiles.items():
                tile_list.extend([k] * v)
            drawnTile = random.choice(tile_list)
            if self.tiles[drawnTile] == 1:
                del self.tiles[drawnTile]
            else:
                self.tiles[drawnTile] -= 1
            return drawnTile

    def add_tile(self, tile):
        if tile in self.tiles:
            self.tiles[tile] += 1
        else:
            self.tiles[tile] = 1

    def exchange_tile(self, tile):
        newTile = self.draw_tile()
        self.add_tile(tile)
        return newTile

    # returns the score value of a given letter tile
    # - to be multiplied with point matrix to calculate points
    def get_value(self, tile):
        return self.tile_values[tile]

    # returns True if Bag still has tiles; False if empty.
    def has_tiles(self):
        return bool(self.tiles)

    def num_tiles(self):
        return sum(self.tiles[tile] for tile in self.tiles)
