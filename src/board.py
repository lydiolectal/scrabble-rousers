from src.trie import TrieNode
from src.crosscheck_square import CrosscheckSquare
from src.coord import Coord
from src.start_seq import StartSequence

class Board:
    def __init__(self, size = 15, trie = None):
        if size < 1 or size % 2 == 0:
            raise RuntimeError(f"Invalid board dimension {size}")
        mid = size // 2
        self.size = size
        self.trie = trie if trie else TrieNode.words()
        self.tiles = [[None] * size for _ in range(size)]
        self.crosschecks = [[CrosscheckSquare() for _ in range(size)] for _ in range(size)]
        self.neighbors = [[False] * size for _ in range(size)]
        self.neighbors[mid][mid] = True
        self.neighbors_set = {(mid, mid)}

    def is_on_board(self, x, y):
        return y >= 0 and y < self.size and x >= 0 and x < self.size

    def get_starts(self, num_tiles):
        starts = []
        for neighbor in self.neighbors_set:
            starts.extend(self.get_start(neighbor, num_tiles, True))
            starts.extend(self.get_start(neighbor, num_tiles, False))
        return starts

    def get_start(self, neighbor, num_tiles, ish):
        starts = []
        start = self.get_start_sequence(neighbor[0], neighbor[1], ish)
        starts.append(start)
        num_tiles -= 1
        dX, dY = (-1, 0) if ish else (0, -1)
        curX, curY = neighbor[0], neighbor[1]
        nextX, nextY = curX + dX, curY + dY

        # if next square is occupied, return the beginning of that word
        if self.is_on_board(nextX, nextY) and self.tiles[nextY][nextX]:
            while self.is_on_board(nextX + dX, nextY + dY) and self.tiles[nextY + dY][nextX + dX] is not None:
                nextX += dX
                nextY += dY
            start = self.get_start_sequence(nextX, nextY, ish)
            return [start]
        else:
            # not edge, not neighbor, still have tiles
            while self.is_on_board(nextX, nextY) and not self.neighbors[nextY][nextX] and num_tiles > 0:
                start = self.get_start_sequence(nextX, nextY, ish)
                starts.append(start)
                if not self.tiles[nextY][nextX]:
                    num_tiles -= 1
                nextX += dX
                nextY += dY
        return starts

    def get_start_sequence(self, startX, startY, ish):
        template = []
        if ish:
            template = [self.tiles[startY][x] for x in range(startX, self.size)]
        else:
            template = [self.tiles[y][startX] for y in range(startY, self.size)]
        return StartSequence(startX, startY, template, ish)

    # cross check board methods
    def get_h_check(self, coord):
        return self.crosschecks[coord.y][coord.x].h_check

    def get_v_check(self, coord):
        return self.crosschecks[coord.y][coord.x].v_check

    def update_state(self, coord, length, ish):
        curX, curY = coord.x, coord.y
        dX, dY = (1, 0) if ish else (0, 1)

        # refactor into boolean function
        if ((ish and curX > 0) or (not ish and curY > 0)) \
        and not self.tiles[curY - dY][curX - dX]:
            # neighbors
            self.neighbors[curY - dY][curX - dX] = True
            self.neighbors_set.add((curX - dX, curY - dY))
            # crosschecks
            template = self.get_update_template(Coord(curX - dX, curY - dY), ish)
            cross_set = self.trie.get_chars(template, self.trie)
            if ish:
                self.crosschecks[curY - dY][curX - dX].h_check = set(cross_set)
            else:
                self.crosschecks[curY - dY][curX - dX].v_check = set(cross_set)
        if ish:
            for curX in range(coord.x, coord.x + length):
                self.update_helper(curX, curY, ish)
        else:
            for curY in range(coord.y, coord.y + length):
                self.update_helper(curX, curY, ish)
        if ((ish and curX < self.size - 1) or (not ish and curY < self.size - 1)) \
        and not self.tiles[curY + dY][curX + dX]:
            self.neighbors[curY + dY][curX + dX] = True
            self.neighbors_set.add((curX + dX, curY + dY))
            template = self.get_update_template(Coord(curX + dX, curY + dY), ish)
            cross_set = self.trie.get_chars(template, self.trie)
            if ish:
                self.crosschecks[curY + dY][curX + dX].h_check = set(cross_set)
            else:
                self.crosschecks[curY + dY][curX + dX].v_check = set(cross_set)

    def update_helper(self, curX, curY, ish):
        dX, dY = (0, 1) if ish else (1, 0)
        self.crosschecks[curY][curX].h_check = set()
        self.crosschecks[curY][curX].v_check = set()
        self.neighbors[curY][curX] = False
        if (curX, curY) in self.neighbors_set:
            self.neighbors_set.remove((curX, curY))
        if (ish and curY > 0) or (not ish and curX > 0):
            self.neighbors[curY - dY][curX - dX] = True
            self.neighbors_set.add((curX - dX, curY - dY))
            if ish:
                # refactor into own function
                template = self.get_update_template(Coord(curX - dX, curY - dY), True)
                cross_set = self.trie.get_chars(template, self.trie)
                self.crosschecks[curY - dY][curY - dY].v_check = set(cross_set)
            else:
                # refactor into own function
                template = self.get_update_template(Coord(curX - dX, curY - dY), False)
                cross_set = self.trie.get_chars(template, self.trie)
                self.crosschecks[curY - dY][curY - dY].h_check = set(cross_set)
        if (ish and curY < self.size - 1) or (not ish and curX < self.size - 1):
            self.neighbors[curY + dY][curX + dX] = True
            self.neighbors_set.add((curX + dX, curY + dY))
            if ish:
                # refactor into own function
                template = self.get_update_template(Coord(curX + dX, curY + dY), True)
                cross_set = self.trie.get_chars(template, self.trie)
                self.crosschecks[curY + dY][curX + dX].v_check = set(cross_set)
            else:
                # refactor into own function
                template = self.get_update_template(Coord(curX + dX, curY + dY), False)
                cross_set = self.trie.get_chars(template, self.trie)
                self.crosschecks[curY + dY][curX + dX].h_check = set(cross_set)

    def get_update_template(self, coord, ish):
        dX, dY = (0, 1) if ish else (1, 0)
        curX, curY = coord.x - dX, coord.y - dY

        template = [None]
        # go left
        while self.is_on_board(curX, curY) and self.tiles[curY][curX]:
            template.insert(0, self.tiles[curY][curX])
            curX -= dX
            curY -= dY
        # go right
        curX, curY = coord.x + dX, coord.y + dY
        while self.is_on_board(curX, curY) and self.tiles[curY][curX]:
            template.append(self.tiles[curY][curX])
            curX += dX
            curY += dY
        return template

    # tile board methods
    def print_b(self):
        for row in self.tiles:
            for col in row:
                if col:
                    print(f" {col} ", end = "")
                else:
                    print(" . ", end = "")
            print()

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
