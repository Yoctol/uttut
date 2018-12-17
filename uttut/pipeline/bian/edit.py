from .validation import _validate_start_end


class Edit:
    '''Represents an edit to a Sequence such as a string or a list

    A sequence is a collection of objects that can be indexed in a linear fashion. E.g. a string

    A edit to a sequence is a replacement of a continuous range of the sequence with the elements
    of the replacement sequence.

    E.g.
    The transformation from "" to "abc": Edit(0, 0, "abc")
    The transformation from "abc" to "aBc": Edit(1, 2, "B")
    The transformation from "aBc" to "aBcdef": Edit(3, 3, "def")
    The transformation from "aBcdef" to "": Edit(0, 6, "")
    Note that insertion at position i is represented as Edit(i, i, ...)
    ("Insertion at i" means that the original i-th element is moved to the right;
     similar to Python's list.insert)

    Args:
        start (int): start index (inclusive)
        end (int): end index (exclusive)
        replacement (obj): the replacement
        annotation (str, optional): an annotation for this edit
    '''

    def __init__(
            self,
            start: int,
            end: int,
            replacement,
            annotation: str = None,
        ):
        _validate_start_end(start, end)
        self.start, self.end = start, end
        self.replacement = replacement
        self.annotation = annotation

    def __eq__(self, other):
        if not isinstance(other, Edit):
            return False
        same_start = other.start == self.start
        same_end = other.end == self.end
        same_replacements = other.replacement == self.replacement
        return same_start and same_end and same_replacements

    def __str__(self):
        return f"({self.start}, {self.end}) => '{self.replacement}'"

    def __repr__(self):
        output_repr = f"Edit({self.start}, {self.end}, " \
            f"{self.replacement}, annotation={self.annotation})"
        return output_repr