# Transformer

Transformation between human-readable dictionary and List of `Datum`.

## Usage

Create a `OrdinalLabel` transformer with its factory method `from_raw_dictionary`:
```python
from uttut.transformers import OrdinalLabel

raw_dict = {
    'data': [
        {
            "utterance": "你好",
            "intent": {
                "names": ["GREETINGS"],
            },
        },
        {
            "utterance": "我想喝珍奶半糖",
            "intent": {
                "names": ["ORDER"],
            },
            "entities": [
                {
                    "name": "ITEM",
                    "start": 3,
                    "end": 5,
                    "replacements": ["拿鐵", "多多綠", "紅茶"],
                },
                {
                    "name": "SUGAR",
                    "start": 5,
                    "end": 7,
                    "replacements": ["無糖", "全糖"],
                },
            ],
        },
        {
            "utterance": "紅茶大杯多少錢",
            "intent": {
                "names": ["ASK_PRICE"],
            },
            "entities": [
                {
                    "name": "ITEM",
                    "start": 0,
                    "end": 2,
                    "replacements": ["珍奶", "多多綠"],
                },
                {
                    "name": "SIZE",
                    "start": 2,
                    "end": 4,
                    "replacements": ["中杯", "小杯"],
                },
            ],
        },
    ]
}

tx = OrdinalLabel.from_raw_dictionary(raw_dict)
```

With it, you can transform
```python
from uttut.elements import Datum, Intent, Entity

raw_datum = {
    "utterance": "早安，我想喝珍奶",
    "intent": {
        "names": ["GREETINGS"],
    },
    "entities": [
        {
            "name": "ITEM",
            "start": 6,
            "end": 8,
        },
    ],
}
datum = Datum(
    utterance="早安，我想喝珍奶",
    intents=[Intent(0)],  # since GREETINGS is the first intent found
    entities=[Entity(
        label=1, # since ITEM is the first entity found, and 0 is preserved for unknown
        value="珍奶",
        start=6,
        end=8,
    )]
)
assert tx.machanize(raw_datum) == datum
assert tx.humanize(datum) == raw_datum
```

For future usage, you may save it through its serialization mechanism:
```python
savable = tx.serialize()  # JSON string

# You may save to FS, blob, DB, etc.
with open('transformer.json', 'w') as fw:
    fw.write(savable)

with open('transformer.json', 'r') as f:
    restored_tx = OrdinalLabel.deserialize(f.read())
```
