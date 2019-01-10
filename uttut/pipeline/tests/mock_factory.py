from typing import List

from ..ops.base import Operator, Realigner
from ..ops.factory import OperatorFactory


class MockRealigner(Realigner):

    def _realign_labels(self, labels: List[int]):
        return labels


class MockStr2StrOp(Operator):

    def __init__(self, **kwargs):
        super().__init__(str, str)

    def __eq__(self, other):
        if not isinstance(other, MockStr2StrOp):
            return False
        return True

    def transform(self, input_sequence: str, labels: List[int]):  # type: ignore
        return input_sequence, labels, MockRealigner(
            edit={},
            input_length=len(input_sequence),
            output_length=len(input_sequence),
        )


class MockLst2LstOp(Operator):

    def __init__(self, **kwargs):
        super().__init__(list, list)

    def __eq__(self, other):
        if not isinstance(other, MockLst2LstOp):
            return False
        return True

    def transform(self, input_sequence: List[str], labels: List[int]):  # type: ignore
        return input_sequence, labels, MockRealigner(
            edit={},
            input_length=len(input_sequence),
            output_length=len(input_sequence),
        )


class MockStr2LstOp(Operator):

    def __init__(self, **kwargs):
        super().__init__(str, list)

    def __eq__(self, other):
        if not isinstance(other, MockStr2LstOp):
            return False
        return True

    def transform(self, input_sequence: str, labels: List[int]):  # type: ignore
        output_sequence = list(input_sequence)
        return output_sequence, labels, MockRealigner(
            edit={},
            input_length=len(output_sequence),
            output_length=len(input_sequence),
        )


mock_factory = OperatorFactory()
mock_factory.register('Str2Str', MockStr2StrOp)
mock_factory.register('Lst2Lst', MockLst2LstOp)
mock_factory.register('Str2Lst', MockStr2LstOp)
