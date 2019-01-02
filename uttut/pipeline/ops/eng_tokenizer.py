from typing import List

import unicodedata

from .tokenizer import Tokenizer


class EngTokenizer(Tokenizer):

    def _tokenize(self, input_str: str) -> List[str]:
        orig_tokens = whitespace_tokenize(input_str)
        split_tokens = []
        for token in orig_tokens:
            split_tokens.extend(self._run_split_on_punc(token))
        output_tokens = whitespace_tokenize(" ".join(split_tokens))
        return output_tokens

    def _run_split_on_punc(self, text: str) -> List[str]:
        """Splits punctuation on a piece of text

        Copy from https://github.com/google-research/bert/blob/master/tokenization.py
        """
        chars = list(text)
        i = 0
        start_new_word = True
        output = []
        while i < len(chars):
            char = chars[i]
            if _is_punctuation(char):
                output.append([char])
                start_new_word = True
            else:
                if start_new_word:
                    output.append([])
                start_new_word = False
                output[-1].append(char)
            i += 1

        return ["".join(x) for x in output]


def whitespace_tokenize(text: str) -> List[str]:
    """Runs basic whitespace cleaning and splitting on a piece of text

    Copy from https://github.com/google-research/bert/blob/master/tokenization.py
    """
    text = text.strip()
    if not text:
        return []
    tokens = text.split()
    return tokens


def _is_punctuation(char):
    """Checks whether `chars` is a punctuation character.

    Copy from https://github.com/google-research/bert/blob/master/tokenization.py

    We treat all non-letter/number ASCII as punctuation.
    Characters such as "^", "$", and "`" are not in the Unicode
    Punctuation class but we treat them as punctuation anyways, for
    consistency.
    """
    cp = ord(char)
    if (
        (cp >= 33 and cp <= 47) or (
            cp >= 58 and cp <= 64) or (
            cp >= 91 and cp <= 96) or (
            cp >= 123 and cp <= 126)
    ):
        return True
    cat = unicodedata.category(char)
    if cat.startswith("P"):
        return True
    return False
