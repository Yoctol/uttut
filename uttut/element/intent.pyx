cdef class Intent:

    def __init__(self, int label):
        self.label = label

    def __repr__(self):
        return f"<Intent {self.label}>"

    def __hash__(self):
        return hash(self.label)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.label == other.label
