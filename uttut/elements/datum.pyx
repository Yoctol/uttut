from .intent cimport Intent
from .entity cimport Entity

from .exceptions import (
    EntityOverlapping,
    EntityPositionError,
)
from .utils cimport (
    entity_position_correct,
    overlap,
    msg_entity_wrong_position,
    msg_entity_overlapping,
)


cdef class Datum:

    def __cinit__(
            self,
            str utterance,
            object intents = None,  # : List[Intent] = None,
            object entities = None,  # : List[Entity] = None,
        ):
        self.utterance = utterance
        self.intents = [] if intents is None else sorted(intents, key=lambda i: hash(i))
        self.entities = [] if entities is None else sorted(entities, key=lambda e: e.start)

        # check entity has correct value and position
        for entity in self.entities:
            if not entity_position_correct(self.utterance, entity):
                raise EntityPositionError(msg_entity_wrong_position(self.utterance, entity))

        # check overlapping entities
        for idx in range(len(self.entities) - 1):
            entity = self.entities[idx]
            next_entity = self.entities[idx + 1]
            if overlap(entity, next_entity):
                raise EntityOverlapping(msg_entity_overlapping(self.utterance, entity, next_entity))

    def __eq__(self, Datum other):
        if not self.has_same_utterance_as(other):
            return False
        if not self.has_same_intents_as(other):
            return False
        if not self.has_same_entities_as(other):
            return False
        return True

    def __repr__(self):
        return "<Datum {} {} with entities: {}>".format(
            self.utterance,
            self.intents,
            self.entities,
        )

    cpdef bint has_same_utterance_as(self, Datum other):
        return self.utterance == other.utterance

    cpdef bint has_same_intents_as(self, Datum other):
        return set(self.intents) == set(other.intents)

    cpdef bint has_same_entities_as(self, Datum other):
        same_entities = False
        if len(self.entities) == len(other.entities):
            for self_entity, other_entity in zip(self.entities, other.entities):
                if self_entity != other_entity:
                    break
            else:
                same_entities = True
        return same_entities

    cpdef bint has_entities(self):
        return len(self.entities) > 0

    cpdef bint has_intents(self):
        return len(self.intents) > 0

    cpdef list copy_intents(self):
        cdef Intent intent
        return [Intent(intent.label) for intent in self.intents]
