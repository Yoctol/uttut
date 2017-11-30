from typing import List

from uttut.elements import Datum


def gen_partitioned_utterance_n_entities(
        datum: Datum,
        not_entity: str = 'DONT_CARE',
    ) -> (List[List[str]], List[List[str]]):

    start = 0
    utterance = datum.utterance
    partitioned_utterance = []
    partitioned_entities = []

    for entity_obj in datum.entities:
        if start != entity_obj.start:
            partitioned_utterance += [
                utterance[start: entity_obj.start]]
            partitioned_entities.append(not_entity)
        partitioned_utterance += [
            utterance[entity_obj.start: entity_obj.end]]
        partitioned_entities.append(entity_obj.name)
        start = entity_obj.end

    if datum.entities[-1].end != len(utterance):
        partitioned_utterance += [utterance[start:]]
        partitioned_entities.append(not_entity)

    if len(partitioned_utterance) != len(partitioned_entities):
        raise KeyError(
            'Number of segments of utterance and entities is not equal',
            'partitioned_utterance = {}, \n partitioned_entities = {}'.format(
                partitioned_utterance, partitioned_entities,
            ),
        )

    return partitioned_utterance, partitioned_entities


def clean_partitioned_utterance_n_entities(
        partitioned_utterance: list,
        partitioned_entities: list,
        tokenizer: object,
        filter_: object = None,
        need_start_end: bool = False,
        not_entity: str = 'DONT_CARE',
    ) -> (List, List):

    if len(partitioned_utterance) != len(partitioned_entities):
        raise ValueError(
            'Length of partitioned_utterance and partitioned_entities should be the same.'
            'Now, partitioned_utterance = {}, partitioned_entities = {}'.format(
                partitioned_utterance,
                partitioned_entities,
            ),
        )

    def filter_n_tokenize(sentence):
        if filter_ is not None:
            return tokenizer.lcut(filter_(sentence))
        else:
            return tokenizer.lcut(sentence)

    tokenized_utterance = []
    entities = []
    for part_of_utterance, entity in zip(partitioned_utterance, partitioned_entities):
        part_of_tokenized_utterance = filter_n_tokenize(part_of_utterance)
        num_tokenized = len(part_of_tokenized_utterance)
        if num_tokenized > 0:
            part_of_entities = [entity] * num_tokenized
            if need_start_end is True:
                if (entity != not_entity) & (num_tokenized > 1):
                    part_of_entities[0] = entity + '_start'
                    part_of_entities[-1] = entity + '_end'
            tokenized_utterance += part_of_tokenized_utterance
            entities += part_of_entities

    assert len(tokenized_utterance) == len(entities)
    return tokenized_utterance, entities
