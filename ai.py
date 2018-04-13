import random, string

class Ai:
    def __init__(self):
        self.tiles = [random.choice(string.ascii_lowercase) for _ in range(7)]

    def make_move(self, board):
        pass

class Board:
    def __init__(self):
        self.rows = [[None] * 15 for _ in range(15)]

    def print_b(self):
        for row in self.rows:
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
        if self.rows[coord.y][coord.x] != None:
            sys.exit("f({coord.x},{coord.y}) has been filled.")

        self.rows[coord.y][coord.x] = letter


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y


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

# instantiate dictionary trie
words = open("scrabble_dictionary.txt").read().lower().splitlines()
trieRoot = TrieNode()
for word in words:
    trieRoot.insert(word)

# select a start word
while True:
    startword = random.choice(words)
    if len(startword) < 15:
        break

# instantiate board and populate w first word
board = Board()
startCoord = Coord(0, 7)
board.place_word(startword, startCoord, True)
board.print_b()

player = Ai()
