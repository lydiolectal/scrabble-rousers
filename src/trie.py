from src.start_seq import StartSequence
from src.trie_node import TrieNode

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, s):
        self.insert_helper(self.root, s, 0)

    def insert_helper(self, node, s, i):
        if i == len(s):
            node.is_word = True
        else:
            curletter = s[i]
            if curletter not in node.children:
                node.children[curletter] = TrieNode()
            self.insert_helper(node.children[curletter], s, i + 1)

    def contains(self, s):
        return self.contains_helper(self.root, s)

    def contains_helper(self, node, s):
        if s == "":
            return node.is_word
        curletter = s[0]
        if curletter in node.children:
            return self.contains_helper(node.children[curletter], s[1:])
        else:
            return False

    # return a StartSequence that includes the word template
    def get_plays_constrained(self, start_seq, tiles, board, dist):
        templates = self.get_words_constrained(start_seq, tiles, board)

        plays = []
        x, y = start_seq.x, start_seq.y
        ish = start_seq.ish
        for template in templates:
            if not all(c is None for c in template) and len(template) >= dist:
                plays.append(StartSequence(x, y, template, ish))
        return plays

    def get_words(self, template):
        return self.get_words_helper(template, self.root)

    def get_chars(self, template):
        # check that there is only one None in the template; error if > 1
        from functools import reduce
        num_blanks = reduce((lambda n, c: n + int(not c)), template, 0)
        if num_blanks != 1:
            raise RuntimeError(f"Template should have 1 blank. {num_blanks} blanks.")
        return self.get_chars_helper(template, self.root)

    def get_words_constrained(self, start_seq, tiles, board):
        s_list = []
        self.get_words_constrained_helper(start_seq, self.root, tiles, board, s_list)
        return s_list

    """
    Gets words that can be played in a given span on the board.
    Parameters:
    -----------
    template: type
    node: type

    Returns:
    --------
    list_of_strings: type

    """
    def get_words_helper(self, template, node, s = ""):
        # while we still have spaces left to fill
        if template != []:
            curspot = template[0]
            if curspot:
                child_words = []
                if curspot in node.children:
                    temps = s + curspot
                    child_words = self.get_words_helper(template[1:],
                        node.children[curspot], temps)
                return child_words
            else:
                words = []
                for next in node.children:
                    temps = s + next
                    child_words = self.get_words_helper(template[1:],
                        node.children[next], temps)
                    if child_words:
                        words.extend(child_words)
                return words
        else:
            if node.is_word:
                return [s]

    # get possible characters for first blank
    def get_chars_helper(self, template, node, c = ""):
        # while we still have spaces left to fill
        if template != []:
            curspot = template[0]
            if curspot:
                child_words = []
                if curspot in node.children:
                    child_words = self.get_chars_helper(template[1:],
                        node.children[curspot], c)
                return child_words
            else:
                chars = []
                for next in node.children:
                    child_words = self.get_chars_helper(template[1:],
                        node.children[next], next)
                    if child_words:
                        chars.extend(child_words)
                return chars
        else:
            if node.is_word:
                return [c]

    def get_words_constrained_helper(self, start_seq, node, tiles, board, s_list, s = []):
        curX, curY = start_seq.x, start_seq.y
        template = start_seq.template
        ish = start_seq.ish

        if template != []:
            curspot = template[0]

            # otherwise, descend trie
            if curspot:
                if curspot in node.children:
                    temps = s + [None]
                    if ish:
                        temp_start_seq = StartSequence(curX + 1, curY, template[1:], ish)
                    else:
                        temp_start_seq = StartSequence(curX, curY + 1, template[1:], ish)
                    child_words = self.get_words_constrained_helper(temp_start_seq,
                        node.children[curspot], tiles, board, s_list, temps)
            else:
                if node.is_word:
                    s_list.append(s)

                crosscheck = board.crosschecks[curY][curX].v_check if ish else board.crosschecks[curY][curX].h_check
                to_traverse = list(crosscheck.intersection(set(tiles)))

                for next in to_traverse:
                    if next in node.children:
                        temps = s + [next]
                        if ish:
                            temp_start_seq = StartSequence(curX + 1, curY, template[1:], ish)
                        else:
                            temp_start_seq = StartSequence(curX, curY + 1 , template[1:], ish)
                        remaining_tiles = tiles[:]
                        remaining_tiles.remove(next)
                        self.get_words_constrained_helper(temp_start_seq,
                            node.children[next], remaining_tiles, board, s_list, temps)
        else:
            if node.is_word:
                s_list.append(s)

    scrabble_words = None

    @staticmethod
    def words():
        if Trie.scrabble_words is None:
            with open("assets/scrabble_dictionary.txt") as f:
                words = f.read().lower().splitlines()
            Trie.scrabble_words = Trie()
            for word in words:
                Trie.scrabble_words.insert(word)
        return Trie.scrabble_words
