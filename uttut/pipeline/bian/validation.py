from typing import Sequence


def validate_start_end(start: int, end: int):

    if not isinstance(start, int) or not isinstance(end, int):
        raise TypeError("start and end must be integers")
    if start < 0 or end < 0:
        raise ValueError("start and end must be positive integers")
    if start > end:
        raise ValueError("start cannot be greater than end")
    return start, end


def validate_objs(objs: Sequence[object], type_):
    '''
    A object must have two integer properties `start` and `end`.
    e.g.
        1. validate a list of edits
            validate_objs([Edit(), ...], Edit)
        2. validate a list of spans
            validate_objs([Span(), ...], Span)
    Returns
        sorted objs
    '''
    _validate_type_of_each_elements(objs, type_)
    return _validate_disjoint(objs)


def _validate_disjoint(objs: Sequence[object]):
    '''
    A object must have two integer properties `start` and `end`.
    '''
    objs = sorted(objs, key=lambda e: e.end)

    current = objs[0].end
    for obj in objs[1:]:
        if obj.start < current:
            raise ValueError(f"overlapped")
        current = obj.end
    return objs


def _validate_type_of_each_elements(objs: Sequence[object], type_):
    for i, element in enumerate(objs):
        if not isinstance(element, type_):
            raise TypeError(f"{i}-th element is not a(an) {type_.__name__}")
