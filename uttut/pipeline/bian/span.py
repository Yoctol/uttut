from .validation import validate_start_end


class Span:
    '''Integer offsets (start_i, end_i) of a sequence

    Args:
        start (int): start index (inclusive)
        end (int): end index (exclusive)
    '''

    def __init__(
            self,
            start: int,
            end: int,
        ):
        self.start, self.end = validate_start_end(start, end)

    def __eq__(self, other):
        if not isinstance(other, Span):
            return False
        same_start = other.start == self.start
        same_end = other.end == self.end
        return same_start and same_end

    def __str__(self):
        return f"({self.start}, {self.end})"

    def __repr__(self):
        return f"Span({self.start}, {self.end})"
