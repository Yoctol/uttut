from unittest import TestCase

from uttut.exceptions import (
    EntityOverlapping,
    EntityPositionError,
)
from ..intent import Intent
from ..entity import Entity
from ..datum import Datum


class ElementDatumTestCase(TestCase):

    def test_raise_entity_position_error_if_entity_position_wrong(self):
        with self.subTest(case='wrong end'):
            with self.assertRaises(EntityPositionError):
                Datum(
                    utterance='去紐約的機票',
                    intents=[Intent(1)],
                    entities=[
                        Entity(label=1, value='紐約', start=1, end=2),
                    ],
                )
        with self.subTest(case='wrong start'):
            with self.assertRaises(EntityPositionError):
                Datum(
                    utterance='去紐約的機票',
                    intents=[Intent(1)],
                    entities=[
                        Entity(label=1, value='紐約', start=0, end=3),
                    ],
                )
        with self.subTest(case='wrong value'):
            with self.assertRaises(EntityPositionError):
                Datum(
                    utterance='去紐曰的機票',
                    intents=[Intent(1)],
                    entities=[Entity(label=1, value='紐約', start=1, end=3)],
                )

    def test_raise_entity_overlap_if_entity_overlaps(self):
        with self.assertRaises(EntityOverlapping):
            Datum(
                utterance='我想吃麥當勞快樂兒童餐',
                intents=[Intent(1)],
                entities=[
                    Entity(label=1, value='快樂', start=6, end=8),
                    Entity(label=2, value='快樂兒童餐', start=6, end=11),
                ],
            )

    def test_entities_correct_order_in_datum(self):
        utterance = '我想訂明天從紐約飛到新加坡的機票'
        entities = [
            Entity(label=1, value='新加坡', start=10,
                   end=13, replacements=['斯堪地那維亞', 'KIX']),
            Entity(label=2, value='明天', start=3,
                   end=5, replacements=['下禮拜二']),
            Entity(label=3, value='紐約', start=6, end=8),
        ]
        intents = [
            Intent(label=1),
        ]
        datum = Datum(
            utterance=utterance,
            intents=intents,
            entities=entities,
        )

        expected_entities = [
            Entity(label=2, value='明天', start=3,
                   end=5, replacements=['下禮拜二']),
            Entity(label=3, value='紐約', start=6, end=8),
            Entity(label=1, value='新加坡', start=10,
                   end=13, replacements=['斯堪地那維亞', 'KIX']),
        ]
        for result_entity, expected_entity in zip(datum.entities, expected_entities):
            self.assertEqual(result_entity.label, expected_entity.label)
            self.assertEqual(result_entity.value, expected_entity.value)
            self.assertEqual(result_entity.start, expected_entity.start)
            self.assertEqual(result_entity.end, expected_entity.end)

    def test_has_entities(self):
        datum = Datum(
            utterance='去紐約的機票',
            intents=[Intent(1)],
            entities=[
                Entity(label=1, value='紐約', start=1, end=3),
            ],
        )
        self.assertTrue(datum.has_entities())

    def test_has_no_entities(self):
        datum = Datum(
            utterance='去紐約的機票',
            intents=[Intent(1)],
            entities=[],
        )
        self.assertFalse(datum.has_entities())

    def test_has_intents(self):
        datum = Datum(
            utterance='去紐約的機票',
            intents=[Intent(1)],
            entities=[
                Entity(label=1, value='紐約', start=1, end=3),
            ],
        )
        self.assertTrue(datum.has_intents())

    def test_has_no_intents(self):
        datum = Datum(
            utterance='去紐約的機票',
            intents=None,
            entities=[
                Entity(label=1, value='紐約', start=1, end=3),
            ],
        )
        self.assertFalse(datum.has_intents())

    def test_same_utterance(self):
        utterance = '我想訂明天從紐約飛到新加坡的機票'
        entities = [
            Entity(label=1, value='新加坡', start=10,
                   end=13, replacements=['斯堪地那維亞', 'KIX']),
            Entity(label=2, value='明天', start=3,
                   end=5, replacements=['下禮拜二']),
            Entity(label=3, value='紐約', start=6, end=8),
        ]
        intents = [
            Intent(label=1),
        ]
        datum = Datum(
            utterance=utterance,
            intents=intents,
            entities=entities,
        )
        datum2 = Datum(
            utterance=utterance,
        )
        self.assertTrue(datum.has_same_utterance_as(datum2))

    def test_same_intents(self):
        utterance = '我想訂明天從紐約飛到新加坡的機票'
        utterance2 = '我想訂機票'
        entities = [
            Entity(label=1, value='新加坡', start=10,
                   end=13, replacements=['斯堪地那維亞', 'KIX']),
            Entity(label=2, value='明天', start=3,
                   end=5, replacements=['下禮拜二']),
            Entity(label=3, value='紐約', start=6, end=8),
        ]
        intents = [
            Intent(label=1),
        ]
        intents2 = [
            Intent(label=1),
        ]
        datum = Datum(
            utterance=utterance,
            intents=intents,
            entities=entities,
        )
        datum2 = Datum(
            utterance=utterance2,
            intents=intents2,
        )
        self.assertTrue(datum.has_same_intents_as(datum2))

    def test_same_entities(self):
        utterance = '我想訂明天從紐約飛到新加坡的機票'
        utterance2 = '我想查明天從紐約飛往新加坡的機票'
        entities = [
            Entity(label=1, value='新加坡', start=10,
                   end=13, replacements=['斯堪地那維亞', 'KIX']),
            Entity(label=2, value='明天', start=3,
                   end=5, replacements=['下禮拜二']),
            Entity(label=3, value='紐約', start=6, end=8),
        ]
        entities2 = [
            Entity(label=1, value='新加坡', start=10,
                   end=13, replacements=['斯堪地那維亞', 'KIX']),
            Entity(label=2, value='明天', start=3,
                   end=5, replacements=['下禮拜二']),
            Entity(label=3, value='紐約', start=6, end=8),
        ]
        intents = [
            Intent(label=1),
        ]
        intents2 = [
            Intent(label=2),
        ]
        datum = Datum(
            utterance=utterance,
            intents=intents,
            entities=entities,
        )
        datum2 = Datum(
            utterance=utterance2,
            intents=intents2,
            entities=entities2,
        )
        self.assertTrue(datum.has_same_entities_as(datum2))

    def test_to_dict(self):
        utterance = "我想訂明天從紐約飛到新加坡的機票"
        intent_labels = [1, 2]
        entity_label = 1
        entity_start = 10
        entity_end = 13
        entity_replacements = ['斯堪地那維亞', 'KIX']
        expected = {
            'utterance': utterance,
            'intent': {'labels': intent_labels},
            'entities': [
                {
                    'label': entity_label,
                    'start': entity_start,
                    'end': entity_end,
                    'replacements': entity_replacements,
                },
            ],
        }
        entity = Entity(
            label=entity_label,
            value='新加坡',
            start=entity_start,
            end=entity_end,
            replacements=entity_replacements,
        )
        actual = Datum(
            utterance=utterance,
            intents=[Intent(label=label) for label in intent_labels],
            entities=[entity],
        ).to_dict()
        self.assertEqual(expected, actual)

    def test_to_dict_without_entities(self):
        utterance = "我想訂明天從紐約飛到新加坡的機票"
        intent_labels = [1, 2]

        expected = {
            'utterance': utterance,
            'intent': {'labels': intent_labels},
        }
        actual = Datum(
            utterance=utterance,
            intents=[Intent(label=label) for label in intent_labels],
            entities=[],
        ).to_dict()
        self.assertEqual(expected, actual)

    def test_to_dict_without_intents(self):
        utterance = "我想訂明天從紐約飛到新加坡的機票"
        entity_label = 1
        entity_start = 10
        entity_end = 13
        entity_replacements = ['斯堪地那維亞', 'KIX']
        expected = {
            'utterance': utterance,
            'intent': {'labels': []},
            'entities': [
                {
                    'label': entity_label,
                    'start': entity_start,
                    'end': entity_end,
                    'replacements': entity_replacements,
                },
            ],
        }
        entity = Entity(
            label=entity_label,
            value='新加坡',
            start=entity_start,
            end=entity_end,
            replacements=entity_replacements,
        )
        actual = Datum(
            utterance=utterance,
            intents=[],
            entities=[entity],
        ).to_dict()

        print(entity)
        self.assertEqual(expected, actual)
