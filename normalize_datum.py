from typing import List, Tuple

from uttut.elements import Datum, Entity
from uttut import ENTITY_LABEL


def _gen_partitioned_utterance_n_entities(
        datum: Datum,
        not_entity: str = ENTITY_LABEL['NOT_ENTITY'],
    ) -> Tuple[List[List[str]], List[List[str]]]:

    start = 0
    utterance = datum.utterance
    partitioned_utterance = []
    partitioned_entities = []

    if datum.has_entities():
        for entity in datum.entities:
            if start != entity.start:
                partitioned_utterance += [
                    utterance[start: entity.start]]
                partitioned_entities.append(not_entity)
            partitioned_utterance += [
                utterance[entity.start: entity.end]]
            partitioned_entities.append(entity.name)
            start = entity.end

        if datum.entities[-1].end != len(utterance):
            partitioned_utterance += [utterance[start:]]
            partitioned_entities.append(not_entity)
    else:
        partitioned_utterance = [utterance]
        partitioned_entities = [not_entity]

    if len(partitioned_utterance) != len(partitioned_entities):
        raise KeyError(
            'Number of segments of utterance and entities is not equal',
            'partitioned_utterance = {}, \n partitioned_entities = {}'.format(
                partitioned_utterance, partitioned_entities,
            ),
        )

    return partitioned_utterance, partitioned_entities


def normalize_datum(
        datum: Datum,
        text_normalizer: object = None,
        not_entity=ENTITY_LABEL['NOT_ENTITY'],
    ) -> Tuple[Datum, List[dict]]:

    if text_normalizer is None:
        return datum, None

    normalized_utterance, meta = text_normalizer.normalize(
        sentence=datum.utterance,
    )
    if not datum.entities:
        return Datum(
            utterance=normalized_utterance,
            intents=datum.intents,
        ), None
    else:
        partitioned_utterance, partitioned_entities = \
            _gen_partitioned_utterance_n_entities(
                datum=datum,
                not_entity=not_entity,
            )
        begin_ind = 0
        entities = []
        entities_ind = 0
        for segment, entity in zip(partitioned_utterance, partitioned_entities):
            normalized_segment, _ = text_normalizer.normalize(
                sentence=segment,
            )
            start = normalized_utterance.find(
                normalized_segment,
                begin_ind,
            )
            if start == -1:
                raise KeyError(
                    'String match fails, str = {}, substr = {}'.format(
                        normalized_utterance,
                        normalized_segment,
                    ),
                )

            begin_ind = start + len(normalized_segment)
            if entity != not_entity:
                entities.append(
                    Entity(
                        name=entity,
                        value=normalized_segment,
                        start=start,
                        end=begin_ind,
                        replacements=datum.entities[entities_ind].replacements,
                    ),
                )
                entities_ind += 1

    return Datum(
        utterance=normalized_utterance,
        intents=datum.intents,
        entities=entities,
    ), meta
