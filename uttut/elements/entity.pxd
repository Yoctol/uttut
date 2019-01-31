cdef class Entity:

    cdef public unsigned int label
    cdef public str value
    cdef public unsigned int start
    cdef public unsigned int end
    cdef public set replacements

    cpdef bint no_replacements(self)
    cpdef unsigned int n_replacements(self)
    cpdef dict to_dict(self)
