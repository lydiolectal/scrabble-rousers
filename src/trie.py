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

    def get_words(self, template):
        return self.get_words_helper(template, self.root)

    def get_chars(self, template):
        return self.get_chars_helper(template, self.root)

    def get_words_tiles(self, template, tiles):
        return self.get_words_tiles_helper(template, self.root, tiles)

    def get_words_constrained(self, start_seq, tiles, board):
        return self.get_words_constrained_helper(start_seq, self.root, tiles, board)

    # get words without tile constraints
    def get_words_helper(self, template, node, s = ""):
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
        # while we still have spaces left to fill
        if template != []:
            curspot = template[0]

            if curspot != None:
                if curspot in node.children:
                    temps = s + curspot
                    child_words = self.get_words_helper(template[1:],
                        node.children[curspot], temps)
                    return child_words
                else:
                    return []

            else:
                words = []
                for next in node.children:
                    temps = s + next
                    child_words = self.get_words_helper(template[1:],
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
    def get_chars_helper(self, template, node, c = ""):
        # while we still have spaces left to fill
        if template != []:
            curspot = template[0]

            if curspot != None:
                if curspot in node.children:
                    child_words = self.get_chars_helper(template[1:],
                        node.children[curspot], c)
                    return child_words
                else:
                    return []

            else:
                words = []
                for next in node.children:
                    child_words = self.get_chars_helper(template[1:],
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
    def get_words_tiles_helper(self, template, node, tiles, s = ""):
        # while we still have spaces left to fill
        if template != []:
            curspot = template[0]

            if curspot != None:
                if curspot in node.children:
                    temps = s + curspot
                    child_words = self.get_words_tiles_helper(template[1:],
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
                        child_words = self.get_words_tiles_helper(template[1:],
                            node.children[next], remaining_tiles, temps)
                        if child_words != []:
                            words.extend(child_words)
                return words
        else:
            if node.is_word:
                return [s]
            else: return []

    def get_words_constrained_helper(self, start_seq, node, tiles, board, s = "", s_list = None):
        if s_list is None:
            s_list = []
        curX, curY = start_seq.x, start_seq.y
        template = start_seq.template
        ish = start_seq.ish

        if template != []:
            curspot = template[0]

            # otherwise, descend trie
            if curspot is not None:
                if curspot in node.children:
                    temps = s + curspot
                    if ish:
                        temp_start_seq = StartSequence(curX + 1, curY, template[1:], ish)
                    else:
                        temp_start_seq = StartSequence(curX, curY + 1 , template[1:], ish)

                    child_words = self.get_words_constrained_helper(temp_start_seq,
                        node.children[curspot], tiles, board, temps, [])
                    if child_words != []:
                        s_list.extend(child_words)
                return s_list

            else:
                # check if this is a valid terminal node
                if node.is_word:
                    s_list.append(s)

                crosscheck = board.crosschecks[curY][curX].v_check if ish else board.crosschecks[curY][curX].h_check
                to_traverse = list(crosscheck.intersection(set(tiles)))

                for next in to_traverse:
                    if next in node.children:
                        temps = s + next
                        if ish:
                            temp_start_seq = StartSequence(curX + 1, curY, template[1:], ish)
                        else:
                            temp_start_seq = StartSequence(curX, curY + 1 , template[1:], ish)
                        remaining_tiles = tiles[:]
                        remaining_tiles.remove(next)
                        child_words = self.get_words_constrained_helper(temp_start_seq,
                            node.children[next], remaining_tiles, board, temps, [])
                        if child_words != []:
                            s_list.extend(child_words)
                return s_list

        else:
            if node.is_word:
                s_list.append(s)
            return s_list

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
