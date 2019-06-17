import re
from typing import List, Tuple

from .base import Operator, NullLabelAligner
from ..edit import lst2lst
from ..edit.replacement import ReplacementGroup
from .tokens import NUM_TOKEN


class PureNumtoToken(Operator):

    _input_type = list
    _output_type = list

    REGEX_PATTERN = re.compile(r"[\d\uFF10-\uFF19]+")

    def __init__(self, token: str = None):
        """
        E.g.
        >>> from uttut.pipeline.ops.span_subwords import SpanSubwords
        >>> op = SpanSubwords(vocab={"I": 0, "apple": 1, "##s": 2}, unk='<unk>', maxlen_per_token=5)
        >>> output_seq, output_labels, realigner = op.transform(["I", "like", "apples"])
        >>> output_labels = label_aligner.transform([1, 2, 3])
        >>> output_seq
        ["I", "<unk>", "apple", "##s"]
        >>> output_labels
        [1, 2, 3, 3]
        >>> label_aligner.inverse_transform(output_labels)
        [1, 2, 3]

        """
        if token is None:
            token = NUM_TOKEN
        self.token = token

    def _transform(self, input_sequence: List[str]) -> Tuple[List[str], 'LabelAligner']:
        forward_replacement_group = self._gen_forward_replacement_group(input_sequence)
        output_sequence = lst2lst.apply(input_sequence, forward_replacement_group)

        label_aligner = PureNumtoTokenAligner(
            input_sequence=input_sequence,
            edit=forward_replacement_group,
            output_length=len(output_sequence),
        )
        return output_sequence, label_aligner

    def _gen_forward_replacement_group(self, input_lst: List[str]) -> ReplacementGroup:
        replacement_group = ReplacementGroup()
        for i, token in enumerate(input_lst):
            # import pdb; pdb.set_trace()
            found_sent = self.REGEX_PATTERN.findall(token)
            if len(found_sent) > 0 and found_sent[0] == token:
                replacement_group.add(
                    start=i,
                    end=i + 1,
                    new_value=[self.token],
                    annotation=f"pure-number-to-token-{self.token}",
                )
        replacement_group.done()

        return replacement_group


PureNumtoTokenAligner = NullLabelAligner
