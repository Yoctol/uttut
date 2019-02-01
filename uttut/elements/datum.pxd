cdef class Datum:  # noqa: E999

    cdef public str utterance
    cdef public list intents
    cdef public list entities

    cpdef bint has_same_utterance_as(self, Datum other)
    cpdef bint has_same_intents_as(self, Datum other)
    cpdef bint has_same_entities_as(self, Datum other)
    cpdef bint has_entities(self)
    cpdef bint has_intents(self)
    cpdef list copy_intents(self)
