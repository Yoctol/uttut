# -*- coding: utf-8 -*-
# import re
from unittest import TestCase
from unittest.mock import call, Mock
from uttut.elements import (
    Datum,
    Intent,
    Entity,
)
from ..normalize_datum import (
    _gen_partitioned_utterance_n_entities,
    normalize_datum,
)


class FakeTextNormalizer(object):

    def normalize(self, sentence):
        return sentence, None


class NormalizeDatumTestCase(TestCase):

    def setUp(self):
        self.example_datum = Datum(
            utterance='家豪大大喜歡吃豪大雞排',
            intents=[Intent(name='favor')],
            entities=[
                Entity(name='brand', value='豪大', start=7, end=9,
                       replacements=['肯德基', '麥噹噹']),
                Entity(name='food', value='雞排', start=9, end=11,
                       replacements=['漢堡', '薯條', '滷肉飯']),
            ],
        )
        self.fake_text_normalizer = FakeTextNormalizer()

    def test__gen_partitioned_utterance_n_entities(self):
        result = _gen_partitioned_utterance_n_entities(
            datum=self.example_datum,
        )
        self.assertEqual(
            (['家豪大大喜歡吃', '豪大', '雞排'], ['DONT_CARE', 'brand', 'food']),
            result,
        )
        result = _gen_partitioned_utterance_n_entities(
            datum=self.example_datum,
            not_entity='HAHAHA',
        )
        self.assertEqual(
            (['家豪大大喜歡吃', '豪大', '雞排'], ['HAHAHA', 'brand', 'food']),
            result,
        )

    def test_normalize_datum_without_normalizer(self):
        result = normalize_datum(
            datum=self.example_datum,
            text_normalizer=None,
        )
        self.assertEqual(
            None,
            result[1],
        )
        self.assertEqual(
            self.example_datum,
            result[0],
        )

    def test_normalize_datum_with_fake_normalizer(self):
        result = normalize_datum(
            datum=self.example_datum,
            text_normalizer=self.fake_text_normalizer,
        )
        self.assertEqual(
            None,
            result[1],
        )
        self.assertEqual(
            self.example_datum,
            result[0],
        )

    def test_normalize_datum_with_mocked_fake_normalizer(self):
        self.fake_text_normalizer.normalize = Mock(return_value=('', None))
        normalize_datum(
            datum=self.example_datum,
            text_normalizer=self.fake_text_normalizer,
        )
        self.fake_text_normalizer.normalize.assert_has_calls(
            [
                call(sentence='家豪大大喜歡吃豪大雞排'),
                call(sentence='家豪大大喜歡吃'),
                call(sentence='豪大'),
                call(sentence='雞排'),
            ],
        )
