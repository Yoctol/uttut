from .intent cimport Intent
from .entity cimport Entity

from .exceptions import (
    EntityOverlapping,
    EntityPositionError,
)
from .utils import (
    entity_position_correct,
    overlap,
    msg_entity_wrong_position,
    msg_entity_overlapping,
)


cdef class Datum:

    def __init__(
            self,
            str utterance,
            list intents = None,  # : List[Intent] = None,
            list entities = None,  # : List[Entity] = None,
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

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError('can only compare datum to datum')

        if not self.has_same_utterance_as(other):
            return False
        elif not self.has_same_intents_as(other):
            return False
        elif not self.has_same_entities_as(other):
            return False
        else:
            return True

    def __repr__(self):
        return "<Datum {} {} with entities: {}>".format(
            self.utterance,
            self.intents,
            self.entities,
        )

    def has_same_utterance_as(self, other):
        return self.utterance == other.utterance

    def has_same_intents_as(self, other):
        return set(self.intents) == set(other.intents)

    def has_same_entities_as(self, other):
        same_entities = False
        if len(self.entities) == len(other.entities):
            for self_entity, other_entity in zip(self.entities, other.entities):
                if self_entity != other_entity:
                    break
            else:
                same_entities = True
        return same_entities

    def has_entities(self):
        return len(self.entities) > 0

    def has_intents(self):
        return len(self.intents) > 0

    def copy_intents(self):
        return [Intent(intent.label) for intent in self.intents]
