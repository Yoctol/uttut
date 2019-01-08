from typing import List

from collections import Counter


def get_most_common(labels: List[int], output_size: int) -> List[int]:
    counter = Counter(labels)
    common_label = counter.most_common()[0][0]
    return [common_label] * output_size


def get_most_common_nonzero(labels: List[int], output_size: int) -> List[int]:
    nonzero_labels = [l for l in labels if l > 0]
    if len(nonzero_labels) == 0:
        return get_zero(labels, output_size)
    return get_most_common(nonzero_labels, output_size)


def get_zero(labels: List[int], output_size: int) -> List[int]:
    return [0] * output_size
