from typing import List


class Intermediate:

    """Collect intermediate products when Pipe run transformation

    attributes:
        collection (list): store input intermediates
        checkpoints (ints): indices of intermediates for query

    """

    def __init__(self, checkpoints: List[int], checkpoint_names: List[str]):
        self.collection: list = []
        self.checkpoints = checkpoints
        self.checkpoint_names = checkpoint_names

    def add(self, intermediate):
        """Append intermediate into self.collection

        Arg:
            intermediate: object to be stored in self.collection

        """
        self.collection.append(intermediate)

    def get_by_checkpoint_index(self, index: int):
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
        """Retrieve intermediate outputs of a pipeline transform by index, slice or checkpoint name

        Arg:
            key (int or slice or str)

        Return:
            intermediates (list)

        Raise:
            IndexError: list index out of range if input index >= len(self.collection)
            KeyError: if checkpoint name is wrong

        """
        if isinstance(key, str):
            try:
                name_to_idx = self.checkpoint_names.index(key)
            except ValueError:
                raise KeyError(
                    "Unknown checkpoint '{}'. Available names: {}".format(key,
                                                                          self.checkpoint_names))
            ck_index = self.checkpoints[name_to_idx]
            return self.collection[ck_index]
        return self.collection[key]
