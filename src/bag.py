# keeps track of tile bag, and allows players to draw and exchange tiles
class Bag:
    def __init__(self):
        self.tiles = {
        "E":12, "A":9, "I":9, "O":8, "N":6, "R":6, "T":6, "L":4, "S":4, "U":4,
        "D":4, "G":3, "B":2, "C":2, "M":2, "P":2, "F":2, "H":2, "V":2, "W":2,
        "Y":2, "K":1, "J":1, "X":1, "Q":1, "Z":1}

        self.tile_values = {
        "E":1, "A":1, "I":1, "O":1, "N":1, "R":1, "T":1, "L":1, "S":1, "U":1,
        "D":2, "G":2, "B":3, "C":3, "M":3, "P":3, "F":4, "H":4, "V":4, "W":4,
        "Y":4, "K":5, "J":8, "X":8, "Q":10, "Z":10}

    # return a letter from the Bag inventory, and delete
    # returns False if Bag is empty
    def draw_tile(self):
        if not(self.has_tiles()):
            return None
        else:
            drawnTile = random.choice(list(self.tiles))
            if self.tiles[drawnTile] == 1:
                del self.tiles[drawnTile]
            else:
                self.tiles[drawnTile] -= 1
            return drawnTile

    def add_tile(self, tile):
        tile = tile.upper()
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
