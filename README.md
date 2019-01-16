# UTTUT

[![travis][travis-image]][travis-url]
[![codecov][codecov-image]][codecov-url]
[![pypi][pypi-image]][pypi-url]
![release][release-image]

[travis-image]: https://img.shields.io/travis/Yoctol/uttut.svg?style=flat
[travis-url]: https://travis-ci.org/Yoctol/uttut
[pypi-image]: https://img.shields.io/pypi/v/uttut.svg?style=flat
[pypi-url]: https://pypi.python.org/pypi/uttut
[codecov-image]: https://codecov.io/gh/Yoctol/uttut/branch/master/graph/badge.svg
[codecov-url]: https://codecov.io/gh/Yoctol/uttut
[release-image]: https://img.shields.io/github/release/Yoctol/uttut.svg


UTTerance UTilities for dialogue system. This package provides some general utils when processing chatbot utterance data.


# Installation

```
$ pip install uttut
```

# Usage

Let's create a Pipe to preprocess a Datum with English utterance.

```python
>>> from uttut.pipeline.pipe import Pipe

>>> p = Pipe()
>>> p.add('IntTokenWithSpace')
>>> p.add('FloatTokenWithSpace')
>>> p.add('MergeWhiteSpaceCharacters')
>>> p.add('StripWhiteSpaceCharacters')
>>> p.add('EngTokenizer')  # word-level (ref: BERT)
>>> p.add('AddSosEos', out='result_of_add_sos_eos')
>>> p.add('Pad', {'maxlen': 5})
>>> p.add(
    'Token2Index',
    {
       'token2index': {
            '<sos>': 0, '<eos>': 1,  # for  AddSosEos
            '<unk>': 2, '<pad>': 3,  # for Pad
            '_int_': 4,  # for IntTokenWithSpace
            '_float_': 5,  # for FloatTokenWithSpace
            'I': 6,
            'apples': 7,
        },
    },
)

>>> from uttut.elements import Datum, Entity, Intent
>>> datum = Datum(
    utterance='I like apples.',
    intents=[Intent(label=1), Intent(label=2)],
    entities=[Entity(start=7, end=13, value='apples', label=7)],
)
>>> output_indices, intent_labels, entity_labels, realigner, intermediate = p.transform(datum)
>>> output_indices
[0, 6, 2, 7, 1, 3, 3]
>>> intent_labels
[1, 2]
>>> entity_labels
[0, 0, 0, 7, 0, 0, 0]
>>> intermediate.get_from_checkpoint('result_of_add_sos_eos')
(["<sos>", "I", "like", "apples", "<eos>"], [0, 0, 0, 7, 0]) 

>>> realigner(entity_labels)
[0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 0] 

```

# Serialization

## Serialize

```python
>>> serialized_str = p.serialize()
```

##  Deserialize 

```python
>>> from uttut.pipeline.pipe import Pipe
>>> p = Pipe.deserialize(serialized_str )
```
