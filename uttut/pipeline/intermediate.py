from typing import List


class Intermediate:

    """Collect intermediate products when Pipe run transformation

    attributes:
        collection (list): store input intermediates
        checkpoints (ints): indices of intermediates for query

    """

    def __init__(self, checkpoints: List[int]):
        self.collection: list
        self.collection = []
        self.checkpoints = checkpoints

    def add(self, intermediate):
        """Append intermediate into self.collection

        Arg:
            intermediate: object to be stored in self.collection

        """
        self.collection.append(intermediate)

    def get(self, index: int = 0):
        """Query intermediate in collection according to input index

        Arg:
            index (int)

        Raise:
            IndexError: list index out of range
            if input index >= len(self.checkpoints) or
            self.checkpoints(index) >= len(self.collection)

        """
        if len(self.checkpoints) == 0:
            return []
        ck_index = self.checkpoints[index]
        return self.collection[ck_index]

    def __getitem__(self, key):
        """Query intermediates by index or slice

        Arg:
            key (int or slice)

        Return:
            intermediates (list)

        Raise:
            IndexError: list index out of range if input index >= len(self.collection)

        """
        return self.collection[key]
