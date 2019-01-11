cdef class Entity:

    cdef public int label
    cdef public str value
    cdef public int start
    cdef public int end
    cdef public set replacements
    cdef public int index