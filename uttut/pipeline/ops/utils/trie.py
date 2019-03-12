class TrieNode:

    def __init__(self):
        self.children = {}
        self.word = None


class Trie:

    def __init__(self):
        self.root = TrieNode()

    def __contains__(self, key):
        return self.exactly_search(key)

    def exactly_search(self, word: str):
        current = self.root
        for char in word:
            if char not in current.children:
                return False
            current = current.children[char]
        if current.word:
            return True
        return False

    def insert(self, word: str):
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.word = word

    def match_prefix(self, word: str, shortest: bool = False, start_idx: int = 0):
        current = self.root
        longest_word = None
        for idx in range(start_idx, len(word)):
            char = word[idx]
            if char not in current.children:
                return longest_word
            current = current.children[char]

            if current.word:
                longest_word = current.word
                if shortest:
                    return longest_word
        return longest_word
