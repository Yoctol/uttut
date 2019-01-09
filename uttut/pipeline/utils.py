from typing import List, Tuple

from uttut.elements import Datum


def unpack_datum(datum: Datum) -> Tuple[str, List[int], List[int]]:

    utterance = datum.utterance
    uttlen = len(utterance)

    # intent
    intent_labels = [intent.label for intent in datum.intents]

    # entity
    entity_labels = [0] * uttlen
    for entity in datum.entities:
        label = entity.label
        for ind in range(entity.start, entity.end):
            entity_labels[ind] = label

    return utterance, intent_labels, entity_labels
