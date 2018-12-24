from typing import List
from .ops.base import Operator


class Step:

    def __init__(self, op: Operator):
        self.op = op

    @property
    def input_type(self):
        return self.op.input_type

    @property
    def output_type(self):
        return self.op.output_type

    def transform(self, input_sequence, labels):
        self.op.reset_bian()
        return self.op.transform(input_sequence, labels)

    def realign_labels(self, labels: List[int]) -> List[int]:
        return self.op.realign_labels(labels)
