from uttut.elements import Datum
from typing import List, Tuple, Union


def partition_by_entities(
        datum: Datum,
        include_orig: bool,
    ) -> Tuple[List[List[str]], List[Union[None, str]]]:

    start = 0
    parts = []
    entity_names = []
    utt = datum.utterance

    for entity in datum.entities:
        if start != entity.start:
            parts.append([utt[start: entity.start]])
            entity_names.append(None)

        if entity.no_replacements():
            part_candidates = [entity.value]
        else:
            part_candidates = sorted(list(entity.replacements))
            if include_orig:
                part_candidates.append(entity.value)
        parts.append(part_candidates)
        entity_names.append(entity.name)

        start = entity.end

    if start != len(utt):
        parts.append([utt[start:]])
        entity_names.append(None)

    return parts, entity_names
