from typing import List

from uttut.elements import Datum


def get_unique_entities(
        data: List[Datum],
        need_start_end: str = False,
    )-> List:
    unique_entities = []
    for datum in data:
        if datum.entities is not None:
            for entity in datum.entities:
                unique_entities.append(entity.name)
    unique_entities = list(set(unique_entities))

    start_end_list = []
    if need_start_end is True:
        for entity in unique_entities:
            start_end_list.append(entity + '_start')
            start_end_list.append(entity + '_end')
        unique_entities += start_end_list

    return unique_entities
