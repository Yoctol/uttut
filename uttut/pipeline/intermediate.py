from typing import List


class Intermediate:

    def __init__(self, checkpoints: List[int]):
        self.collection: list
        self.collection = []
        self.checkpoints = checkpoints

    def add(self, intermediate):
        self.collection.append(intermediate)

    def get(self, index: int = 0):
        if len(self.checkpoints) == 0:
            return []
        ck_index = self.checkpoints[index]
        return self.collection[ck_index]

    def __getitem__(self, index: int):
        return self.collection[index]
