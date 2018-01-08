from typing import List, Tuple

from nlu.entity_utils.nested_data_partition import (
    gen_partitioned_utterance,
    augment_single_partition_utterances,
)
from .elements import (
    Datum,
    Entity,
)


__all__ = [
    'expand_by_entities',
]


def partition_by_entities(datum: Datum) -> Tuple[List[dict], List[dict]]:
    entities = [entity.to_dict() for entity in datum.entities]
    new_entities, parts = gen_partitioned_utterance(
        sorted_entities=entities,
        utterance=datum.utterance,
    )
    return new_entities, parts


def _include_orig_value(
        entities_with_index: List[dict],
        parts: List[str],
    ) -> List[dict]:
    new_entities = entities_with_index.copy()
    for entity in new_entities:
        target_idx = entity['index']
        replacements = entity.get('replacements', [])
        replacements.append(parts[target_idx])
        entity['replacements'] = replacements
    return new_entities


def _aggregate_entities(
        parts: List[str],
        entities_with_index: List[dict],
    ) -> List[Entity]:
    index2entity = {
        obj['index']: obj
        for obj in entities_with_index
    }

    entities = []
    pointer = 0
    for idx, part in enumerate(parts):
        len_part = len(part)
        if idx in index2entity:
            entity = index2entity[idx]
            replacements = set(entity.get('replacements')) - set([part])
            entities.append(Entity(
                name=entity['name'],
                value=part,
                start=pointer,
                end=pointer + len_part,
                replacements=replacements,
            ))
        pointer += len_part
    return entities


def expand_by_entities(datum: Datum) -> List[Datum]:
    if not datum.has_entities():
        return [datum]
    entities_with_index, parts = partition_by_entities(datum)

    augmented_parts = augment_single_partition_utterances(
        partitioned_utterance=parts,
        sorted_entities=entities_with_index,
    )

    included_entities_with_index = _include_orig_value(entities_with_index, parts)

    result = []
    for parts in augmented_parts:
        utterance = ''.join(parts)
        entities = _aggregate_entities(parts, included_entities_with_index)
        new_datum = Datum(
            utterance=utterance,
            intents=datum.copy_intents(),
            entities=entities,
        )
        result.append(new_datum)
    return result
