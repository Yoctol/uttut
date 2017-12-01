# -*- coding: utf-8 -*-
import re
from django.test import TestCase

from uttut.elements import (
    Datum,
    Intent,
    Entity,
)
from ..handle_partitioned_utterance_n_entities import (
    gen_partitioned_utterance_n_entities,
    clean_partitioned_utterance_n_entities,
)


class FakeTokenizer(object):

    def lcut(self, sentence):
        return list(sentence)


def fakefilter(sentence):
    return re.sub('[.!,:;\*\^\$#@~\{\}]+', '', sentence)


class HandlePartitionedUtteranceNEntitiesTestCase(TestCase):

    def setUp(self):
        self.intents = [Intent(name='favor')]
        self.entities = [
            Entity(name='brand', value='豪大', start=7, end=9,
                   replacements=['肯德基', '麥噹噹']),
            Entity(name='food', value='雞排', start=9, end=11,
                   replacements=['漢堡', '薯條', '滷肉飯']),
        ]
        self.example_datum = Datum(
            utterance='家豪大大喜歡吃豪大雞排',
            intents=self.intents,
            entities=self.entities,
        )
        self.example_tokenizer = FakeTokenizer()
        self.example_filter = fakefilter

    def test_gen_partitioned_utterance_n_entities(self):
        result = gen_partitioned_utterance_n_entities(
            datum=self.example_datum,
        )
        self.assertEqual(
            (['家豪大大喜歡吃', '豪大', '雞排'], ['DONT_CARE', 'brand', 'food']),
            result,
        )

        result = gen_partitioned_utterance_n_entities(
            datum=self.example_datum,
            not_entity='HAHAHA',
        )
        self.assertEqual(
            (['家豪大大喜歡吃', '豪大', '雞排'], ['HAHAHA', 'brand', 'food']),
            result,
        )

    def test_clean_partitioned_utterance_n_entities(self):
        self.example_partitioned_utterance = ['家豪大大喜歡吃', '豪大', '雞排']
        self.example_partitioned_entities = ['DONT_CARE', 'brand', 'food']
        result = clean_partitioned_utterance_n_entities(
            partitioned_utterance=self.example_partitioned_utterance,
            partitioned_entities=self.example_partitioned_entities,
            tokenizer=self.example_tokenizer,
        )
        self.assertEqual(
            (['家', '豪', '大', '大', '喜', '歡', '吃', '豪', '大', '雞', '排'],
             ['DONT_CARE', 'DONT_CARE', 'DONT_CARE', 'DONT_CARE',
              'DONT_CARE', 'DONT_CARE', 'DONT_CARE', 'brand', 'brand',
              'food', 'food']),
            result,
        )
        with self.assertRaises(ValueError):
            result = clean_partitioned_utterance_n_entities(
                partitioned_utterance=self.example_partitioned_utterance,
                partitioned_entities=['DONT_CARE', 'brand'],
                tokenizer=self.example_tokenizer,
            )

        with self.assertRaises(ValueError):
            result = clean_partitioned_utterance_n_entities(
                partitioned_utterance=['家豪大大喜歡吃', '豪大', '雞排', 'XD'],
                partitioned_entities=self.example_partitioned_entities,
                tokenizer=self.example_tokenizer,
            )

        result = clean_partitioned_utterance_n_entities(
            partitioned_utterance=self.example_partitioned_utterance,
            partitioned_entities=self.example_partitioned_entities,
            tokenizer=self.example_tokenizer,
            need_start_end=True,
        )
        self.assertEqual(
            (['家', '豪', '大', '大', '喜', '歡', '吃', '豪', '大', '雞', '排'],
             ['DONT_CARE', 'DONT_CARE', 'DONT_CARE', 'DONT_CARE',
              'DONT_CARE', 'DONT_CARE', 'DONT_CARE', 'brand_START', 'brand_END',
              'food_START', 'food_END']),
            result,
        )

        result = clean_partitioned_utterance_n_entities(
            partitioned_utterance=['::家豪;;大大!!喜歡吃*^#^*',
                                   '{*豪大*}', '@@雞@排@@', '!!*@*!!'],
            partitioned_entities=['DONT_CARE', 'brand', 'food', 'DONT_CARE'],
            filter_=self.example_filter,
            tokenizer=self.example_tokenizer,
        )
        self.assertEqual(
            (['家', '豪', '大', '大', '喜', '歡', '吃', '豪', '大', '雞', '排'],
             ['DONT_CARE', 'DONT_CARE', 'DONT_CARE', 'DONT_CARE',
              'DONT_CARE', 'DONT_CARE', 'DONT_CARE', 'brand', 'brand',
              'food', 'food']),
            result,
        )
