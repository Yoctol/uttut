from .entity cimport Entity


cdef bint entity_position_correct(str utterance, Entity entity):
    cdef unsigned int start, end
    start = entity.start
    end = entity.end
    if entity.value == utterance[start: end]:
        return True
    return False


cdef bint overlap(Entity entity, Entity next_entity):
    return entity.end > next_entity.start


cdef str msg_entity_wrong_position(str utterance, Entity entity):
    cdef unsigned int start, end
    start = entity.start
    end = entity.end
    return """
        Utterance position {start} - {end} expected to be {expected},
        but got {result}.
    """.format(
        start=start,
        end=end,
        expected=entity.value,
        result=utterance[start: end],
    )


cdef str msg_entity_overlapping(str utterance: str, Entity entity, Entity next_entity):
    return """
        For utterance {utt}, entity {sv} ends at {se}, and entity {nv} starts at {ns},
        which are overlapping. Currently, uttut doesn't support overlapping or hierachy entities.
    """.format(
        utt=utterance,
        sv=entity.value,
        se=entity.end,
        nv=next_entity.value,
        ns=next_entity.start,
    )
