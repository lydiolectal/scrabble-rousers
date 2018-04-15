import unittest

# class Trie():
#     pass

class TrieNode():
    def __init__(self):
        self.is_word = False
        self.children = {}

    def add_entry(self, s):
        if s == "":
            self.is_word = True
        else:
            curletter = s[0]
            if curletter not in self.children:
                self.children[curletter] = TrieNode()
            self.children[curletter].add_entry(s[1:])

    def contains(self, s):
        if s == "":
            return True
        curletter = s[0]
        if curletter in self.children:
            return self.children[curletter].contains(s[1:])
        else:
            return False

class TestTrie(unittest.TestCase):
    def test_twoletter(self):
        t = TrieNode()
        d = "jo"
        t.add_entry(d)
        c_node = t.children['j']
        self.assertFalse(c_node.is_word)
        self.assertTrue(c_node.children["o"].is_word)

    def test_threeletter(self):
        t = TrieNode()
        d = "suq"
        t.add_entry(d)
        s_node = t.children["s"]
        u_node = s_node.children["u"]
        q_node = u_node.children["q"]
        self.assertFalse(s_node.is_word)
        self.assertFalse(u_node.is_word)
        self.assertTrue(q_node.is_word)
        self.assertEqual(len(t.children), 1)

    def test_dictionary(self):
        # instantiate dictionary trie
        with open("scrabble_dictionary.txt") as f:
            words = f.read().lower().splitlines()
        trieRoot = TrieNode()
        for word in words:
            trieRoot.add_entry(word)

        # print all children of 'aa'
        # aa_node = trieRoot.children["a"].children["a"]
        # result = []
        # for key in aa_node.children.keys():
        #     result.append(key)
        # self.assertEqual(result, ["h", "l", "r", "s"])
        self.assertTrue(trieRoot.contains("zyzzyvas"))

    def test_contains(self):
        t = TrieNode()
        t.add_entry("undulate")
        self.assertTrue(t.contains("undulate"))
