import unittest
import random, string

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
    def __init__(self):
        self.tiles = [[None] * 15 for _ in range(15)]
        self.crosschecks = [[CrosscheckSquare() for _ in range(15)] for _ in range(15)]

    # cross check board methods
    def get_h_check(self, coord):
        return self.crosschecks[coord.y][coord.x].h_check

    def get_v_check(self, coord):
        return self.crosschecks[coord.y][coord.x].v_check

    def update_helper_h(self, coord):
        curX, curY = coord.x-1, coord.y
        template = [None]
        # go left
        while curX >= 0 and self.tiles[curY][curX] != None:
            template.insert(0, self.tiles[curY][curX])
            curX -= 1

        # go right
        curX, curY = coord.x+1, coord.y
        while curX <= 14 and self.tiles[curY][curX] != None:
            template.append(self.tiles[curY][curX])
            curX += 1
        return template

    def update_helper_v(self, coord):
        curX, curY = coord.x, coord.y-1
        template = [None]
        # go left
        while curY >= 0 and self.tiles[curY][curX] != None:
            template.insert(0, self.tiles[curY][curX])
            curY -= 1

        # go right
        curX, curY = coord.x, coord.y+1
        while curY <= 14 and self.tiles[curY][curX] != None:
            template.append(self.tiles[curY][curX])
            curY += 1
        return template

    # update appropriate crosscheck sets for a new word with coordinates coord,
    # position position, horizontal orientation ish.
    def update_crosschecks(self, coord, length, ish, trie):
        if ish:
            curY = coord.y
            curX = coord.x
            if not curX == 0 and self.tiles[curY][curX-1] == None:
                template = self.update_helper_h(Coord(curX - 1, curY))
                cross_set = trie.get_chars(template, trie)
                self.crosschecks[curY][curX-1].h_check = set(cross_set)

            for curX in range(coord.x, coord.x + length):
                self.crosschecks[curY][curX].h_check = set()
                self.crosschecks[curY][curX].v_check = set()

                if coord.y > 0:
                    template = self.update_helper_v(Coord(curX, curY-1))
                    cross_set = trie.get_chars(template, trie)
                    self.crosschecks[curY-1][curX].v_check = set(cross_set)
                if coord.y < 14:
                    template = self.update_helper_v(Coord(curX, curY+1))
                    cross_set = trie.get_chars(template, trie)
                    self.crosschecks[curY+1][curX].v_check = set(cross_set)

            if not curX == 14 and self.tiles[curY][curX+1] == None:
                template = self.update_helper_h(Coord(curX + 1, curY))
                cross_set = trie.get_chars(template, trie)
                self.crosschecks[curY][curX+1].h_check = set(cross_set)
        else:
            curY = coord.y
            curX = coord.x
            if not curY == 0 and self.tiles[curY-1][curX] == None:
                template = self.update_helper_v(Coord(curX, curY - 1))
                cross_set = trie.get_chars(template, trie)
                self.crosschecks[curY-1][curX].v_check = set(cross_set)

            for curY in range(coord.y, coord.y + length):
                self.crosschecks[curY][curX].h_check = set()
                self.crosschecks[curY][curX].v_check = set()

                if coord.x > 0:
                    template = self.update_helper_h(Coord(curX - 1, curY))
                    cross_set = trie.get_chars(template, trie)
                    self.crosschecks[curY][curX - 1].h_check = set(cross_set)
                if coord.x < 14:
                    template = self.update_helper_h(Coord(curX + 1, curY))
                    cross_set = trie.get_chars(template, trie)
                    self.crosschecks[curY][curX + 1].h_check = set(cross_set)

            if not curY == 14 and self.tiles[curY + 1][curX] == None:
                template = self.update_helper_v(Coord(curX, curY + 1))
                cross_set = trie.get_chars(template, trie)
                self.crosschecks[curY+1][curX].v_check = set(cross_set)

    # tile board methods
    def print_b(self):
        for row in self.tiles:
            for col in row:
                if col == None:
                    print(" . ", end = "")
                else:
                    print(f" {col} ", end = "")
            print()

    # assume that no words go out of range.
    def place_word(self, word, coord, ish):
        if word == "":
            return
        self.place_letter(word[0], coord)
        if ish:
            coord = Coord(coord.x+1, coord.y)
        else:
            coord = Coord(coord.x, coord.y+1)
        self.place_word(word[1:], coord, ish)

    def place_letter(self, letter, coord):
        if self.tiles[coord.y][coord.x] != None:
            sys.exit("f({coord.x},{coord.y}) has been filled.")

        self.tiles[coord.y][coord.x] = letter

class TrieNode:
    def __init__(self):
        self.is_word = False
        self.children = {}

    def insert(self, s):
        if s == "":
            self.is_word = True
        else:
            curletter = s[0]
            if curletter not in self.children:
                self.children[curletter] = TrieNode()
            self.children[curletter].insert(s[1:])

    def contains(self, s):
        if s == "":
            return True
        curletter = s[0]
        if curletter in self.children:
            return self.children[curletter].contains(s[1:])
        else:
            return False

    # get words without tile constraints
    def get_words(self, template, node, s = ""):
        # while we still have spaces left to fill
        if template != []:
            curspot = template[0]

            if curspot != None:
                if curspot in node.children:
                    temps = s + curspot
                    child_words = self.get_words(template[1:],
                        node.children[curspot], temps)
                    return child_words
                else:
                    return []

            else:
                words = []
                for next in node.children:
                    temps = s + next
                    child_words = self.get_words(template[1:],
                        node.children[next], temps)
                    if child_words != []:
                        words.extend(child_words)
                return words
        else:
            if node.is_word:
                return [s]
            else:
                return []

    # get possible characters for first blank
    def get_chars(self, template, node, c = ""):
        # while we still have spaces left to fill
        if template != []:
            curspot = template[0]

            if curspot != None:
                if curspot in node.children:
                    child_words = self.get_chars(template[1:],
                        node.children[curspot], c)
                    return child_words
                else:
                    return []

            else:
                words = []
                for next in node.children:
                    child_words = self.get_chars(template[1:],
                        node.children[next], next)
                    if child_words != []:
                        words.extend(child_words)
                return words
        else:
            if node.is_word:
                return [c]
            else:
                return []

    # get words given tile rack
    def get_words_tiles(self, template, node, tiles, s = ""):
        # while we still have spaces left to fill
        if template != []:
            curspot = template[0]

            if curspot != None:
                if curspot in node.children:
                    temps = s + curspot
                    child_words = self.get_words_tiles(template[1:],
                        node.children[curspot], tiles, temps)
                    return child_words
                else:
                    return []

            else:
                to_traverse = list(set(tiles))
                words = []
                for next in to_traverse:
                    if next in node.children:
                        temps = s + next
                        remaining_tiles = tiles[:]
                        remaining_tiles.remove(next)
                        child_words = self.get_words_tiles(template[1:],
                            node.children[next], remaining_tiles, temps)
                        if child_words != []:
                            words.extend(child_words)
                return words
        else:
            if node.is_word:
                return [s]
            else: return []


class Ai:
    def __init__(self):
        # self.tiles = [random.choice(string.ascii_lowercase) for _ in range(7)]
        self.tiles = ["c", "a", "s", "u", "k", "m", "p", "e", "d", "r", "s",
        "i", "t", "o"]

    def make_move(self, board):
        pass
    def get_positions(self, board):
        pass
class TestAi(unittest.TestCase):

    # def test_getpositions(self):
    #
    #     # select a start word
    #     startword = "cabriole"
    #
    #     # instantiate board and populate w first word
    #     board = Board()
    #     startCoord = Coord(3, 7)
    #     board.place_word(startword, startCoord, True)
    #     board.print_b()
    #
    #     player = Ai()
    #     self.assertTrue(True)

    def test_getwords(self):
        # instantiate dictionary trie
        with open("scrabble_dictionary.txt") as f:
            words = f.read().lower().splitlines()
        trieRoot = TrieNode()
        for word in words:
            trieRoot.insert(word)

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
        with open("scrabble_dictionary.txt") as f:
            words = f.read().lower().splitlines()
        trieRoot = TrieNode()
        for word in words:
            trieRoot.insert(word)

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
        board.update_crosschecks(startCoord, len(startWord), True, trieRoot)
        board.print_b()
        # after placing "cabriole" at (7,3), v crosscheck for (8, 4) should be:
        expected = {'i', 's', 'e', 'w', 'g', 'm', 'n', 'l', 'd', 'a', 'y', 'x',
                    't', 'h', 'r'}
        self.assertEqual(board.get_v_check(testCoord), expected)

        board = Board()
        board.place_word(startWord, Coord(7, 3), False)
        board.update_crosschecks(Coord(7, 3), len(startWord), False, trieRoot)
        self.assertEqual(board.get_h_check(Coord(8, 4)), expected)

    def test_getchar(self):
        with open("scrabble_dictionary.txt") as f:
            words = f.read().lower().splitlines()
        trieRoot = TrieNode()
        for word in words:
            trieRoot.insert(word)

        template = ["c", "a", "b", None, "i", "o", "l", "e"]
        self.assertEqual(trieRoot.get_chars(template, trieRoot), ["r"])
        template = ["c", "a", None]
        print(trieRoot.get_chars(template, trieRoot))
