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

    tokenized_utterance = []
    entities = []
    for part_of_utterance, entity in zip(partitioned_utterance, partitioned_entities):
        part_of_tokenized_utterance = _filter_n_tokenize(
            sentence=part_of_utterance,
            tokenizer=tokenizer,
            filter_=filter_,
        )
        num_tokenized = len(part_of_tokenized_utterance)
        if num_tokenized > 0:
            part_of_entities = [entity] * num_tokenized
            if need_start_end is True:
                if (entity != not_entity) & (num_tokenized > 1):
                    part_of_entities[0] = entity + '_start'
                    part_of_entities[-1] = entity + '_end'
            tokenized_utterance += part_of_tokenized_utterance
            entities += part_of_entities

    if len(tokenized_utterance) != len(entities):
        raise KeyError(
            'Number of segments of tokenized utterance and entities is not equal',
            'tokenized_utterance = {}, \n entities = {}'.format(
                tokenized_utterance, entities,
            ),
        )

    return tokenized_utterance, entities


def _filter_n_tokenize(
        sentence: str,
        tokenizer: object,
        filter_=None,
    ):
    if filter_ is not None:
        return tokenizer.lcut(filter_(sentence))
    else:
        return tokenizer.lcut(sentence)
