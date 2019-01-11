from ..utils import unpack_datum

from uttut.elements import Datum, Intent, Entity


def test_unpack_datum():
    utterance = '我想訂明天從紐約飛到新加坡的機票'
    entities = [
        Entity(label=1, value='新加坡', start=10,
               end=13, replacements=['斯堪地那維亞', 'KIX']),
        Entity(label=2, value='明天', start=3,
               end=5, replacements=['下禮拜二']),
        Entity(label=3, value='紐約', start=6, end=8),
    ]
    intents = [Intent(1)]
    datum = Datum(
        utterance=utterance,
        intents=intents,
        entities=entities,
    )
    output_utt, output_intent, output_entity = unpack_datum(datum)

    assert utterance == output_utt
    assert [1] == output_intent
    assert [0, 0, 0, 2, 2, 0, 3, 3, 0, 0, 1, 1, 1, 0, 0, 0] == output_entity
