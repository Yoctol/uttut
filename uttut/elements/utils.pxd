from .entity cimport Entity  # noqa: E999

cdef bint entity_position_correct(str utterance, Entity entity)
cdef bint overlap(Entity entity, Entity next_entity)
cdef str msg_entity_wrong_position(str utterance, Entity entity)
cdef str msg_entity_overlapping(str utterance: str, Entity entity, Entity next_entity)
