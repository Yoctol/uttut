# -*- coding: utf-8 -*-
from unittest import TestCase
from unittest.mock import Mock
from uttut.elements import (
    Datum,
    Intent,
    Entity,
)
from ..tokenize_datum import (
    tokenize_datum,
    _get_entity_array,
)


class TokenizeDatumTestCase(TestCase):

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
        self.fake_tokenizer = Mock()

    def test__get_entity_array(self):
        result = _get_entity_array(
            datum=self.example_datum,
        )
        self.assertEqual(
            ['DONT_CARE', 'DONT_CARE', 'DONT_CARE', 'DONT_CARE', 'DONT_CARE',
             'DONT_CARE', 'DONT_CARE', 'brand', 'brand', 'food', 'food'],
            result,
        )

    def test_tokenize_datum(self):
        self.fake_tokenizer.lcut = Mock(
            return_value=['家豪大大喜歡吃豪', '大雞排'],
        )
        result = tokenize_datum(
            datum=self.example_datum,
            tokenizer=self.fake_tokenizer,
        )
        self.assertEqual(
            ['brand', 'food'],
            result[1],
        )
        self.fake_tokenizer.lcut = Mock(
            return_value=['家豪大大', '喜歡吃豪', '大雞', '排'],
        )
        result = tokenize_datum(
            datum=self.example_datum,
            tokenizer=self.fake_tokenizer,
        )
        self.assertEqual(
            ['DONT_CARE', 'brand', 'food', 'food'],
            result[1],
        )
