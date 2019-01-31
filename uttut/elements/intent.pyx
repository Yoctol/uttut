cdef class Intent:  # noqa: E999

    def __cinit__(self, int label):
        self.label = label

    def __repr__(self):
        return f"<Intent {self.label}>"

    def __hash__(self):
        return hash(self.label)

    def __eq__(self, Intent other):
        return self.label == other.label
