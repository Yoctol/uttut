from typing import Sequence


def _validate_start_end(start: int, end: int):

    if not isinstance(start, int) or not isinstance(end, int):
        raise TypeError("start and end must be integers")
    if start < 0 or end < 0:
        raise ValueError("start and end must be positive integers")
    if start > end:
        raise ValueError("start cannot be greater than end")


def _validate_disjoint(sorted_objs: Sequence[object]):
    '''
    An object must have two integer properties `start` and `end`.
    '''
    current = sorted_objs[0].end  # type: ignore
    for obj in sorted_objs[1:]:
        if obj.start < current:  # type: ignore
            raise ValueError(f"overlapped")
        current = obj.end  # type: ignore


def _validate_type_of_each_elements(objs: Sequence[object]):
    target_type = type(objs[0])
    for i, element in enumerate(objs):
        if not isinstance(element, target_type):
            raise TypeError(f"{i}-th element is not a(an) {target_type.__name__}")
