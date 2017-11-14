from typing import List, Iterable

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


class Entity:

    def __init__(
            self,
            name: str,
            value: str,
            start: int,
            end: int,
            replacements: Iterable[str] = None,
        ) -> None:
        self.name = name
        self.value = value
        self.start = start
        self.end = end
        replacements = [] if replacements is None else replacements
        self.replacements = set(replacements)

    def no_replacements(self) -> bool:
        return len(self.replacements) == 0

    def to_legacy_entity(self) -> dict:
        result = {
            'name': self.name,
            'start': self.start,
            'end': self.end - 1,
        }
        if not self.no_replacements():
            result['replacements'] = list(self.replacements)
        return result

    @classmethod
    def from_legacy_entity(cls, entity: dict, utterance: str):
        new_end = entity['end'] + 1
        entity_value = utterance[entity['start']: new_end]
        replacements = entity.get('replacements')
        return cls(
            name=entity['name'],
            value=entity_value,
            start=entity['start'],
            end=new_end,
            replacements=[] if replacements is None else replacements,
        )


class Intent:

    def __init__(self, intent: str) -> None:
        self.intent = intent

    def __hash__(self):
        return hash(self.intent)


class Datum:

    def __init__(
            self,
            utterance: str,
            intents: List[Intent],
            entities: List[Entity] = None,
        ) -> None:
        self.utterance = utterance
        self.intents = [] if intents is None else intents
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

    def has_entities(self) -> bool:
        return len(self.entities) > 0

    def has_intents(self) -> bool:
        return len(self.intents) > 0

    @classmethod
    def load_from_legacy_shape(cls, utterance_obj):
        utterance = utterance_obj['utterance']
        intents = [Intent(utterance_obj['intent'])]  # legacy shape has only one intent
        entities = None
        if utterance_obj.get('entities') is not None:
            entities = []
            for entity in utterance_obj['entities']:
                entities.append(Entity.from_legacy_entity(entity, utterance_obj['utterance']))
        return cls(
            utterance=utterance,
            intents=intents,
            entities=entities,
        )
