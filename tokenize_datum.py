from typing import List

from uttut.elements import Datum
from uttut import ENTITY_LABEL

from collections import Counter


def _get_entity_array(
        datum: Datum,
        not_entity: str = ENTITY_LABEL['NOT_ENTITY'],
    ):
    result = [not_entity] * len(datum.utterance)
    for entity in datum.entities:
        for ind in range(entity.start, entity.end):
            result[ind] = entity.name
    return result


def tokenize_datum(
        datum: Datum,
        tokenizer: object,
        not_entity: str = ENTITY_LABEL['NOT_ENTITY'],
    ) -> (List[str], List[str]):

    tokenized_utterance = tokenizer.lcut(datum.utterance)
    entity_array = _get_entity_array(
        datum=datum,
        not_entity=not_entity,
    )
    entities = []
    begin_ind = 0
    for token in tokenized_utterance:
        entity_stat = Counter(
            entity_array[begin_ind: begin_ind + len(token)],
        )
        entity_stat = sorted(entity_stat.items(), key=lambda x: (-x[1], x[0]))
        if (entity_stat[0][0] == not_entity) and (len(entity_stat) > 1):
            entities.append(entity_stat[1][0])
        else:
            entities.append(entity_stat[0][0])
        begin_ind += len(token)
    return tokenized_utterance, entities
