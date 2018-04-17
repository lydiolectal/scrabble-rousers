import unittest
import random, string

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class CrosscheckSquare:
    def __init__(self):
        self.h_check = set()
        self.v_check = set()

class Board:
    def __init__(self):
        # board for tiles that have been played; tracks game state
        self.tiles = [[None] * 15 for _ in range(15)]
        # board for crosschecking adjacent spaces of preexisting words.
        self.crosschecks = [[CrosscheckSquare() for _ in range(15)] for _ in range(15)]

    # cross check board methods
    def get_h_check(self, coord):
        return self.crosschecks[coord.y][coord.x].h_check

    def get_v_check(self, coord):
        return self.crosschecks[coord.y][coord.x].v_check

    # update appropriate crosscheck sets for a new word with coordinates coord,
    # position position, horizontal orientation ish.
    def update(self, coord, position, ish):
        # TODO: this.
        if ish:
            # for first, check if left is edge or filled


            # if not, feed [None] + position.
            # for each letter, check if top or bottom is edge or filled
            # if not, feed [None] + square or square + [None]. splice
            # for the set of legal characters.
            # for first, check if left is edge or filled
            # if not, feed position + [None]

            pass
        else:
            # same thing, but replace top/bottom with left/right and v-versa.
            pass

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

class Ai:
    def __init__(self):
        # self.tiles = [random.choice(string.ascii_lowercase) for _ in range(7)]
        self.tiles = ["c", "a", "s", "u", "k", "m", "p", "e", "d", "r", "s",
        "i", "t", "o"]

    def make_move(self, board):
        pass
        # positions, coord = get_positions()
        # words = get_words(positions)
        # play each word on temp board, return the word that maximizes score.

    def get_words(self, position, node, tiles, s):
        # while we still have spaces left to fill
        if position != []:
            curspot = position[0]

            if curspot != None:
                if curspot in node.children:
                    temps = s + curspot
                    child_words = self.get_words(position[1:],
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
                        child_words = self.get_words(position[1:],
                            node.children[next], remaining_tiles, temps)
                        if child_words != []:
                            words.extend(child_words)
                return words
        else:
            if node.is_word:
                return [s]
            else: return []


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

        position = ["a", "b", "a", None, None, None]
        expected = []
        with open("sample.txt") as f:
            for line in f.read().splitlines():
                if len(line) == 6:
                    expected.append(line)
        # we expect: ['abacas', 'abacus', 'abakas', 'abamps', 'abased',
        #'abaser', 'abases', 'abasia', 'abated', 'abater', 'abates',
        #'abatis', 'abator']

        player = Ai()
        actual = player.get_words(position, trieRoot, player.tiles, "")

        self.assertEqual(sorted(actual), sorted(expected))
        self.assertEqual(len(expected), len(actual))

    def test_crosscheck(self):
        crosscheck_board = Crosscheck()

        testCoord = Coord(8, 4)
        # should be empty set
        self.assertEqual(crosscheck_board.get_v_check(testCoord), set())

        startword = "cabriole"
        board = Board()
        startCoord = Coord(3, 7)
        board.place_word(startword, startCoord, True)

        # TODO: call update!
        # after placing "cabriole" at (7,3), v crosscheck for (8, 4) should be:
        expected = {'i', 's', 'e', 'w', 'g', 'm', 'n', 'l', 'd', 'a', 'y', 'x',
                    't', 'h', 'r'}
        self.assertEqual(crosscheck_board.get_v_check(testCoord), expected)
