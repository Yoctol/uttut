from unittest import TestCase

from .. import ENTITY_LABEL
from ..elements import (
    Datum,
    Entity,
)
from ..exceptions import DifferentUtterance

from ..entity_overlapping_ratio import (
    check_utter_index_in_entity,
    expand_entity_with_list,
    penalty_on_same_entity_or_not,
    entity_overlapping_ratio,
)

NOT_ENTITY = ENTITY_LABEL['NOT_ENTITY']


class EntityOverlappingRatioTestCase(TestCase):

    def test_check_utter_index_in_entity(self):
        entity = Entity(name='GOD', value='CPH', start=0, end=2)
        ent_list = []
        utter_ind = 1
        result = check_utter_index_in_entity(utter_ind, entity, ent_list)
        self.assertEqual(result, True)

    def test_expand_entity_with_list(self):
        datum = Datum(
            utterance='家豪大大',
            intents=[],
            entities=[
                Entity(name='GOD', value='家豪', start=0, end=2),
            ],
        )
        ans_ent_list = ['GOD', 'GOD', NOT_ENTITY, NOT_ENTITY]
        test_ent_list = expand_entity_with_list(datum)
        self.assertListEqual(test_ent_list, ans_ent_list)

    def test_penalty_on_same_entity_or_not(self):
        ent1 = NOT_ENTITY
        ent2 = 'CPH'
        pen1 = penalty_on_same_entity_or_not(ent1, ent2, 5)
        self.assertEqual(pen1, 1)

        ent1 = 'cph'
        ent2 = 'hoa'
        pen2 = penalty_on_same_entity_or_not(ent1, ent2, 5)
        self.assertEqual(pen2, 5)

        ent1 = 'CPH'
        ent2 = 'CPH'
        pen3 = penalty_on_same_entity_or_not(ent1, ent2, 5)
        self.assertEqual(pen3, 0)

    def test_raise_if_diff_utt(self):
        datum1 = Datum(
            utterance='家豪大大喜歡吃豪大大雞排',
            intents=[],
            entities=[
                Entity(name='GOD', value='家豪', start=0, end=2),
            ],
        )
        datum2 = Datum(
            utterance='家豪大喜歡吃豪大大雞排',
            intents=[],
            entities=[
                Entity(name='GOD', value='家豪', start=0, end=2),
            ],
        )
        with self.assertRaises(DifferentUtterance):
            entity_overlapping_ratio(datum1, datum2, 2)

    def test_score_1(self):
        datum1 = Datum(
            utterance='家豪大大喜歡吃豪大大雞排',
            intents=[],
            entities=[
                Entity(name='GOD', value='家豪', start=0, end=2),
                Entity(name='BRAND', value='豪大', start=7, end=9),
                Entity(name='FOOD_SIZE', value='大', start=9, end=10),
                Entity(name='FOOD', value='雞排', start=10, end=12),
            ],
        )
        datum2 = Datum(
            utterance='家豪大大喜歡吃豪大大雞排',
            intents=[],
            entities=[
                Entity(name='GOD', value='家豪', start=0, end=2),
                Entity(name='BRAND', value='豪大', start=7, end=9),
                Entity(name='FOOD_SIZE', value='大', start=9, end=10),
                Entity(name='FOOD', value='雞排', start=10, end=12),
            ],
        )

        ratio = entity_overlapping_ratio(datum1, datum2, 2)
        self.assertEqual(ratio, 1.0)

    def test_score_0(self):
        datum1 = Datum(
            utterance='吃豪大大雞排',
            intents=[],
            entities=[
                Entity(name='BRAND', value='豪大', start=1, end=3),
                Entity(name='FOOD_SIZE', value='大', start=3, end=4),
                Entity(name='FOOD', value='雞排', start=4, end=6),
            ],
        )
        datum2 = Datum(
            utterance='吃豪大大雞排',
            intents=[],
            entities=[
                Entity(name='BRAND', value='豪大', start=1, end=3),
                Entity(name='FOOD_ITEM', value='大雞排', start=3, end=6),
            ],
        )

        ratio = entity_overlapping_ratio(datum1, datum2, 2)
        self.assertEqual(ratio, 0.0)

    def test_score_between_0_1(self):
        datum1 = Datum(
            utterance='家豪大大喜歡吃豪大大雞排',
            intents=[],
            entities=[
                Entity(name='GOD', value='家豪', start=0, end=2),
                Entity(name='BIG', value='大', start=9, end=10),
                Entity(name='FOOD', value='雞排', start=10, end=12),
            ],
        )
        datum2 = Datum(
            utterance='家豪大大喜歡吃豪大大雞排',
            intents=[],
            entities=[
                Entity(name='GOD', value='家豪', start=0, end=2),
                Entity(name='FOOD_ITEM', value='大雞排', start=9, end=12),
            ],
        )

        ratio = entity_overlapping_ratio(datum1, datum2, 2)
        self.assertEqual(ratio, 0.5)
