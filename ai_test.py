import unittest
import random, string
from trie import TrieNode
from start_seq import StartSequence


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class CrosscheckSquare:
    def __init__(self):
        # initial possible things that can be played is every letter.
        self.h_check = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
            'x', 'y', 'z'}
        self.v_check = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
            'x', 'y', 'z'}

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
        if self.is_on_board(nextX, nextY) and self.tiles[nextY][nextX] is not None:
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
                if self.tiles[nextY][nextX] is None:
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

        if ((ish and curX > 0) or (not ish and curY > 0)) \
        and self.tiles[curY - dY][curX - dX] is None:
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
        and self.tiles[curY + dY][curX + dX] is None:
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
                template = self.get_update_template(Coord(curX - dX, curY - dY), True)
                cross_set = self.trie.get_chars(template, self.trie)
                self.crosschecks[curY - dY][curY - dY].v_check = set(cross_set)
            else:
                template = self.get_update_template(Coord(curX - dX, curY - dY), False)
                cross_set = self.trie.get_chars(template, self.trie)
                self.crosschecks[curY - dY][curY - dY].h_check = set(cross_set)
        if (ish and curY < self.size - 1) or (not ish and curX < self.size - 1):
            self.neighbors[curY + dY][curX + dX] = True
            self.neighbors_set.add((curX + dX, curY + dY))
            if ish:
                template = self.get_update_template(Coord(curX + dX, curY + dY), True)
                cross_set = self.trie.get_chars(template, self.trie)
                self.crosschecks[curY + dY][curX + dX].v_check = set(cross_set)
            else:
                template = self.get_update_template(Coord(curX + dX, curY + dY), False)
                cross_set = self.trie.get_chars(template, self.trie)
                self.crosschecks[curY + dY][curX + dX].h_check = set(cross_set)

    def get_update_template(self, coord, ish):
        dX, dY = (0, 1) if ish else (1, 0)
        curX, curY = coord.x - dX, coord.y - dY

        template = [None]
        # go left
        while self.is_on_board(curX, curY) and self.tiles[curY][curX] is not None:
            template.insert(0, self.tiles[curY][curX])
            curX -= dX
            curY -= dY
        # go right
        curX, curY = coord.x + dX, coord.y + dY
        while self.is_on_board(curX, curY) and self.tiles[curY][curX] is not None:
            template.append(self.tiles[curY][curX])
            curX += dX
            curY += dY
        return template

    # tile board methods
    def print_b(self):
        for row in self.tiles:
            for col in row:
                if col == None:
                    print(" . ", end = "")
                else:
                    print(f" {col} ", end = "")
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
        if letter != None:
            if self.tiles[coord.y][coord.x] != None:
                sys.exit("f({coord.x},{coord.y}) has been filled.")
            self.tiles[coord.y][coord.x] = letter


class Ai:
    def __init__(self):
        # self.tiles = [random.choice(string.ascii_lowercase) for _ in range(7)]
        self.tiles = ["c", "a", "s", "u", "k", "m", "p", "e", "d", "r", "s",
        "i", "t", "o"]

    def make_move(self, board):
        pass

class TestAi(unittest.TestCase):

    def test_place_word(self):
        word_template = [c for c in "cabr"] + [None] + [c for c in "iole"]
        startCoord = Coord(3, 7)
        board = Board()
        board.place_word(word_template, startCoord, True)
        self.assertEqual(board.tiles[7][7], None)

    def test_getwords(self):
        trieRoot = TrieNode.words()

        template = ["a", "b", "a", None, None, None]
        expected = []
        with open("sample.txt") as f:
            for line in f.read().splitlines():
                if len(line) == 6:
                    expected.append(line)
        # we expect: ['abacas', 'abacus', 'abakas', 'abamps', 'abased',
        #'abaser', 'abases', 'abasia', 'abated', 'abater', 'abates',
        #'abatis', 'abator']

        player = Ai()
        actual = trieRoot.get_words_tiles(template, trieRoot, player.tiles)

        self.assertEqual(sorted(actual), sorted(expected))
        self.assertEqual(len(expected), len(actual))

        actual = trieRoot.get_words(template, trieRoot)
        self.assertEqual(sorted(actual), sorted(expected))
        self.assertEqual(len(expected), len(actual))

    def test_crosscheck(self):
        trieRoot = TrieNode.words()

        board = Board()
        testCoord = Coord(4, 8)
        # should be empty set
        expected = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
            'x', 'y', 'z'}
        self.assertEqual(board.get_v_check(testCoord), expected)

        startWord = "cabriole"
        startCoord = Coord(3, 7)
        board.place_word(startWord, startCoord, True)
        board.update_state(startCoord, len(startWord), True)
        # after placing "cabriole" at (7,3), v crosscheck for (8, 4) should be:
        expected = {'i', 's', 'e', 'w', 'g', 'm', 'n', 'l', 'd', 'a', 'y', 'x',
                    't', 'h', 'r'}
        self.assertEqual(board.get_v_check(testCoord), expected)

        board = Board()
        board.place_word(startWord, Coord(7, 3), False)
        board.update_state(Coord(7, 3), len(startWord), False)
        self.assertEqual(board.get_h_check(Coord(8, 4)), expected)

    def test_getchar(self):
        trieRoot = TrieNode.words()

        template = ["c", "a", "b", None, "i", "o", "l", "e"]
        self.assertEqual(trieRoot.get_chars(template, trieRoot), ["r"])
        template = ["c", "a", None]
        # print(trieRoot.get_chars(template, trieRoot))

    def test_update_neighbors(self):

        trieRoot = TrieNode.words()

        board = Board()
        testCoord = Coord(4, 8)
        startWord = "cabriole"
        startCoord = Coord(3, 7)
        board.place_word(startWord, startCoord, True)
        board.update_state(startCoord, len(startWord), True)
        # not a neighbor
        self.assertEqual(board.neighbors[9][4], False)
        # occupied
        self.assertEqual(board.neighbors[7][6], False)
        # should be neighbors
        self.assertEqual(board.neighbors[7][2], True)
        self.assertEqual(board.neighbors[6][9], True)
        self.assertEqual(board.neighbors[8][9], True)
        self.assertEqual(board.neighbors[7][11], True)

        starts = board.get_starts(5)
        # for start in starts:
        #     print(f"({start.x}, {start.y}): {start.template}")

        tiles = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

        start = StartSequence(4, 6, [None, "a", None, None, None, None, None, None, None], False)
        plays = trieRoot.get_words_constrained(start, trieRoot, tiles, board)
        # print("Times called: ", times_called)
        # print("Number of words: ", len(plays))
        # print(plays)

    # test that board gets proper start positions
    def test_get_starts(self):
        from collections import Counter

        b1 = Board(1)
        starts = b1.get_starts(1)
        self.assertEqual(len(starts), 2)
        start_coors = {(0,0)}
        self.assertEqual(start_coors, {(s.x, s.y) for s in starts})

        self.assertRaises(RuntimeError, lambda: Board(2))

        b2 = Board(3)
        starts = b2.get_starts(2)
        self.assertEqual(len(starts), 4)
        start_coors = {(1,1), (0,1), (1,0)}
        self.assertEqual(start_coors, {(s.x, s.y) for s in starts})
        c = Counter(s.ish for s in starts)
        self.assertEqual(c[True], 2)
        self.assertEqual(c[False], 2)

    def test_get_start_occupied(self):
        b3 = Board(5)
        b3.place(["a", "a"], Coord(1, 2), True)
        starts = b3.get_starts(2)

        def is_horizontal(start):
            return start.x == 1 and start.y == 2 and start.ish
        def is_vertical(start):
            return start.x == 1 and start.y == 2 and not start.ish
        self.assertEqual(len(list(filter(is_horizontal, starts))), 1)
        self.assertEqual(len(list(filter(is_vertical, starts))), 1)

        self.assertEqual(len(starts), 18)

    def test_update(self):
        b4 = Board(5)
        b4.place(["b", "u", "g"], Coord(2, 1), False)
        b4.print_b()

        # neighbors
        self.assertEqual(b4.neighbors_set, {(1, 1), (1, 2), (1, 3), (2, 0),
                                            (2, 4), (3, 1), (3, 2), (3, 3)})
        self.assertFalse(b4.neighbors[1][2])
        self.assertTrue(b4.neighbors[2][3])

        # crosschecks
        self.assertEqual(b4.crosschecks[1][2].h_check, set())
        self.assertEqual(b4.crosschecks[1][3].h_check, {"a", "e", "i", "o", "y"})
