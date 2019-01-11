cdef class Intent:

    def __init__(self, int label):
        self.label = label

    def __repr__(self):
        return str(self.label)

    def __hash__(self):
        return hash(self.label)

    def __eq__(self, other):
        return self.label == other.label
