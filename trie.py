from start_seq import StartSequence

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

    def get_words_constrained(self, start_seq, node, tiles, board, s = "", s_list = None):
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

                    child_words = self.get_words_constrained(temp_start_seq,
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
                        child_words = self.get_words_constrained(temp_start_seq,
                            node.children[next], remaining_tiles, board, temps, [])
                        if child_words != []:
                            s_list.extend(child_words)
                return s_list

        else:
            if node.is_word:
                s_list.append(s)
            return s_list
