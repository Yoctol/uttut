from typing import List, Tuple, Dict

from .tokens import UNK_TOKEN
from .base import Operator, Realigner
from .label_transducer import get_most_common, get_most_common_except_not_entity
from ..edit import lst2lst
from ..edit.replacement import ReplacementGroup
from ..edit.label_propagation import propagate_by_replacement_group


class SpanSubwords(Operator):

    def __init__(
            self,
            vocab: Dict[str, int],
            unk_token: str = UNK_TOKEN,
            maxlen_per_token: int = 200,
        ):

        """
        Span each element in input_sequence to several subwords according to the input vocabulary.

        If the element or part of element is not found in vocabulary,
        the unk_token would be returned.

        ## Requirement: All elements in input_sequence should not contain
                        whitespaces and accent tokens.

        This class is almost the same as WordPieceTokenizer in BERT.
        ref: https://github.com/google-research/bert/blob/master/tokenization.py

        E.g.
        >>> from uttut.pipeline.ops.span_subwords import SpanSubwords
        >>> op = SpanSubwords(vocab={"I": 0, "apple": 1, "##s": 2}, unk='<unk>', maxlen_per_token=5)
        >>> output_seq, output_labels, realigner = op.transform(["I", "like", "apples"], [1, 2, 3])
        >>> output_seq
        ["I", "<unk>", "apple", "##s"]
        >>> output_labels
        [1, 2, 3, 3]
        >>> realigner(output_labels)
        [1, 2, 3]

        """

        super().__init__(input_type=list, output_type=list)
        self.vocab = vocab
        self.unk_token = unk_token
        self.maxlen_per_token = maxlen_per_token
        self._realigner_class = WordPieceRealigner

    def __eq__(self, other):
        same_vocab = self.vocab == other.vocab
        same_unk_token = self.unk_token == other.unk_token
        same_maxlen_per_token = self.maxlen_per_token == other.maxlen_per_token
        return same_vocab and same_unk_token and same_maxlen_per_token and super().__eq__(other)

    def transform(  # type: ignore
            self,
            input_sequence: List[str],
            labels: List[int],
        ) -> Tuple[List[str], List[int], 'Realigner']:

        """
        ## Requirement: All elements in input_sequence should not contain
                        whitespaces and accent tokens.
        """

        forward_replacement_group = self._gen_forward_replacement_group(input_sequence)
        output_sequence = lst2lst.apply(input_sequence, forward_replacement_group)
        inverse_replacement_group = lst2lst.inverse(input_sequence, forward_replacement_group)

        updated_labels = propagate_by_replacement_group(
            labels, forward_replacement_group, self._forward_reduce_func)

        realigner = self._realigner_class(
            edit=inverse_replacement_group,
            input_length=len(output_sequence),
            output_length=len(input_sequence),
        )

        return output_sequence, updated_labels, realigner

    def _gen_forward_replacement_group(self, input_lst: List[str]) -> ReplacementGroup:

        replacement_group = ReplacementGroup()
        for i, token in enumerate(input_lst):
            subtokens = span_subwords(
                word=token,
                unk_token=self.unk_token,
                vocab=self.vocab,
                max_input_chars_per_word=self.maxlen_per_token,
            )
            if subtokens != [token]:
                replacement_group.add(
                    start=i,
                    end=i + 1,
                    new_value=subtokens,
                    annotation='span-subwords',
                )
        replacement_group.done()

        return replacement_group

    def _forward_reduce_func(self, labels: List[int], output_size: int):
        return get_most_common(labels, output_size)


class WordPieceRealigner(Realigner):

    def _backward_transduce_func(self, labels: List[int], output_size: int) -> List[int]:
        return get_most_common_except_not_entity(labels, output_size)

    def _realign_labels(self, labels: List[int]) -> List[int]:
        return propagate_by_replacement_group(labels, self._edit, self._backward_transduce_func)


def span_subwords(
        word: str,
        unk_token: str,
        vocab: Dict[str, int],
        max_input_chars_per_word: int,
    ) -> List[str]:

    """
    Tokenize a word into several subwords.

    This code is copied from Bert tokenization.py.

    Requirement: The input word should not contain whitespaces and accent tokens.

    This uses a greedy longest-match-first algorithm to perform tokenization
    using the given vocabulary.

    The default arguments in BERT are
    unk_token = '[UNK]'
    max_input_chars_per_word = 200

    E.g.
    >>> span_subwords(
            word="unaffable",
            vocab={"un": 0, "##aff": 1, "##able": 2},
            max_input_chars_per_word=200,
        )
    ["un", "##aff", "##able"]

    """

    # length of word is more than expected -> return [unk_token]
    if len(word) > max_input_chars_per_word:
        return [unk_token]

    # subword matching
    chars = list(word)
    is_bad = False
    start = 0
    sub_tokens = []
    while start < len(chars):
        end = len(chars)
        cur_substr = None
        while start < end:
            substr = "".join(chars[start: end])
            if start > 0:
                substr = "##" + substr
            if substr in vocab:
                cur_substr = substr
                break
            end -= 1
        if cur_substr is None:
            is_bad = True
            break
        sub_tokens.append(cur_substr)
        start = end

    if is_bad:
        # one of subwords is not in vocab
        return [unk_token]
    return sub_tokens
