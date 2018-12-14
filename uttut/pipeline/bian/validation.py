def validate_start_end(start: int, end: int):

    if not isinstance(start, int) or not isinstance(end, int):
        raise TypeError("start and end must be integers")
    if start < 0 or end < 0:
        raise ValueError("start and end must be positive integers")
    if start > end:
        raise ValueError("start cannot be greater than end")
    return start, end
