class TrieNode:

    def __init__(self):
        self._children = {}
        self._word = None

    def has_child(self, key):
        if key in self._children:
            return True
        return False

    def get_child(self, key):
        return self._children[key]

    def insert_child(self, key):
        self._children[key] = TrieNode()

    def set_word(self, word):
        self._word = word

    def get_word(self):
        return self._word


class Trie:

    def __init__(self):
        self.root = TrieNode()

    def __contains__(self, key):
        return self.exactly_search(key)

    def exactly_search(self, word: str):
        current = self.root
        for char in word:
            if not current.has_child(char):
                return False
            current = current.get_child(char)
        if current.get_word():
            return True
        return False

    def insert(self, word: str):
        current = self.root
        for char in word:
            if not current.has_child(char):
                current.insert_child(char)
            current = current.get_child(char)
        current.set_word(word)

    def match_prefix(self, word: str, shortest: bool = False, start_idx: int = 0):
        current = self.root
        longest_word = None
        for idx in range(start_idx, len(word)):
            char = word[idx]
            if not current.has_child(char):
                return longest_word
            current = current.get_child(char)

            if current.get_word():
                longest_word = current.get_word()
                if shortest:
                    return longest_word
        return longest_word
