from src.trie import Trie
from src.crosscheck_square import CrosscheckSquare
from src.coord import Coord
from src.start_seq import StartSequence

import sys

class Board:
    def __init__(self, size = 15, trie = None):
        if size < 1 or size % 2 == 0:
            raise RuntimeError(f"Invalid board dimension {size}")
        mid = size // 2
        self.size = size

        self.trie = trie if trie else Trie.words()
        self.tiles = [[None] * size for _ in range(size)]
        self.crosschecks = [[CrosscheckSquare() for _ in range(size)] for _ in range(size)]

        self.neighbors = [[False] * size for _ in range(size)]
        self.neighbors[mid][mid] = True
        self.neighbors_set = {Coord(mid, mid)}

    def is_on_board(self, coord):
        x, y = coord
        return 0 <= y < self.size and 0 <= x < self.size

    def get_starts(self, num_tiles):
        starts = []
        for neighbor in self.neighbors_set:
            starts.extend(self.get_start(neighbor, num_tiles, True))
            starts.extend(self.get_start(neighbor, num_tiles, False))
        return starts

    def get_start(self, neighbor, num_tiles, ish):
        starts = []
        curX, curY = neighbor
        dX, dY = (-1, 0) if ish else (0, -1)
        num_tiles -= 1
        tiles_used = 1

        start = self.get_start_sequence(Coord(curX, curY), ish, tiles_used)
        starts.append(start)
        nextX, nextY = curX + dX, curY + dY

        # if next square is occupied, traverse until beginning of that word
        if self.is_on_board(Coord(nextX, nextY)) and self.tiles[nextY][nextX]:
            while self.is_on_board(Coord(nextX + dX, nextY + dY)) and self.tiles[nextY + dY][nextX + dX] is not None:
                nextX += dX
                nextY += dY
            start = self.get_start_sequence(Coord(nextX, nextY), ish, tiles_used)
            return [start]
        # if next square is empty, traverse until you run out of tiles, hit edge
        # or hit another neighbor
        else:
            while self.is_on_board(Coord(nextX, nextY)) and not self.neighbors[nextY][nextX] and num_tiles > 0:
                if not self.tiles[nextY][nextX]:
                    num_tiles -= 1
                    tiles_used += 1
                start = self.get_start_sequence(Coord(nextX, nextY), ish, tiles_used)
                starts.append(start)
                nextX += dX
                nextY += dY
        return starts

    def get_start_sequence(self, coord, ish, dist):
        startX, startY = coord
        template = []
        if ish:
            template = [self.tiles[startY][x] for x in range(startX, self.size)]
        else:
            template = [self.tiles[y][startX] for y in range(startY, self.size)]
        return StartSequence(startX, startY, template, ish, dist)

    # cross check board methods
    def get_h_check(self, coord):
        return self.crosschecks[coord.y][coord.x].h_check

    def get_v_check(self, coord):
        return self.crosschecks[coord.y][coord.x].v_check

    def is_edge(self, coord, ish, is_increment):
        if is_increment:
            return (ish and coord.x >= self.size - 1) or (not ish and coord.y >= self.size - 1)
        else:
            return (ish and coord.x <= 0) or (not ish and coord.y <= 0)

    def in_word(self, coord, word_end, ish):
        if ish:
            return coord.x < word_end
        else:
            return coord.y < word_end

    def update_state(self, coord, word_length, ish):
        x, y = coord
        self.update_helper(Coord(x, y), ish, False)

        curX, curY = coord
        dX, dY = (1, 0) if ish else (0, 1)
        word_end = curX + word_length if ish else curY + word_length

        while self.in_word(Coord(curX, curY), word_end, ish):
            self.update_helper(Coord(curX, curY), not ish, False)
            self.update_helper(Coord(curX, curY), not ish, True)

            self.neighbors[curY][curX] = False
            if (curX, curY) in self.neighbors_set:
                self.neighbors_set.remove(Coord(curX, curY))
            self.crosschecks[curY][curX].empty()
            curX += dX
            curY += dY

        x = x + dX * (word_length - 1)
        y = y + dY * (word_length - 1)
        self.update_helper(Coord(x, y), ish, True)

    def update_helper(self, coord, ish, is_increment):
        x, y = coord
        if is_increment:
            dX, dY = (1, 0) if ish else (0, 1)
        else:
            dX, dY = (-1, 0) if ish else (0, -1)

        # check that it's not an edge and the square is unoccupied
        if not self.is_edge(coord, ish, is_increment) and not self.tiles[y + dY][x + dX]:
            self.neighbors[y + dY][x + dX] = True
            self.neighbors_set.add(Coord(x + dX, y + dY))
            template = self.get_update_template(Coord(x + dX, y + dY), ish)
            cross_set = self.trie.get_chars(template)
            self.crosschecks[y + dY][x + dX].set_crosscheck(set(cross_set), ish)

    def get_update_template(self, coord, ish):
        dX, dY = (1, 0) if ish else (0, 1)
        x, y = coord.x - dX, coord.y - dY
        template = [None]
        # go left
        while self.is_on_board(Coord(x, y)) and self.tiles[y][x]:
            template.insert(0, self.tiles[y][x])
            x -= dX
            y -= dY
        # go right
        x, y = coord.x + dX, coord.y + dY
        while self.is_on_board(Coord(x, y)) and self.tiles[y][x]:
            template.append(self.tiles[y][x])
            x += dX
            y += dY
        return template

    def place(self, word_template, coord, ish):
        self.place_word(word_template, coord, ish)
        self.update_state(coord, len(word_template), ish)

    def place_word(self, word_template, coord, ish):
        if len(word_template) == 0:
            return
        self.place_letter(word_template[0], coord)
        if ish:
            coord = Coord(coord.x+1, coord.y)
        else:
            coord = Coord(coord.x, coord.y+1)
        self.place_word(word_template[1:], coord, ish)

    def place_letter(self, letter, coord):
        if letter:
            if self.tiles[coord.y][coord.x]:
                sys.exit("f({coord.x},{coord.y}) has been filled.")
            self.tiles[coord.y][coord.x] = letter

    # tile board methods
    def print_b(self):
        for row in self.tiles:
            for col in row:
                if col:
                    print(f" {col} ", end = "")
                else:
                    print(" . ", end = "")
            print()
