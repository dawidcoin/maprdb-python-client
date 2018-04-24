from __future__ import unicode_literals

import json
from datetime import datetime

from decimal import Decimal

from ojai.o_types.OInterval import OInterval
from mapr.ojai.ojai.OJAIDocument import OJAIDocument
from ojai.o_types.ODate import ODate
from ojai.o_types.OTime import OTime
from ojai.o_types.OTimestamp import OTimestamp

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class DocumentTagsTest(unittest.TestCase):

    def test_empty_doc(self):
        doc = OJAIDocument()
        self.assertTrue(doc.empty())
        self.assertEqual(doc.as_dictionary(), {})

    def test_doc_insert_id(self):
        doc = OJAIDocument()
        doc.set_id("75")
        self.assertEqual(doc.get_id(), "75")
        self.assertEqual(type(doc.get_id()), unicode)
        doc.set_id(str("75"))
        self.assertEqual(doc.get_id(), "75")
        self.assertEqual(type(doc.get_id()), str)

        self.assertEqual(doc.as_dictionary(), {'_id': "75"})

    def test_doc_set_date(self):
        doc = OJAIDocument()
        doc.set("today", ODate(days_since_epoch=3456))
        self.assertEqual(doc.as_json_str(), '{"today": {"$dateDay": "1979-06-19"}}')
        doc.set_id("6123")
        self.assertEqual(doc.as_json_str(), '{"_id": "6123", "today": {"$dateDay": "1979-06-19"}}')

    def test_doc_set_time(self):
        doc1 = OJAIDocument().set("test_time", OTime(timestamp=1518689532)).set_id('121212')
        doc2 = OJAIDocument().set("test_time", OTime(hour_of_day=12, minutes=12, seconds=12)).set_id('121212')
        doc3 = OJAIDocument().set("test_time", OTime(date=datetime(year=1999, month=12, day=31, hour=12, minute=12,
                                                                   second=12))).set_id("121212")
        self.assertEqual(doc1.as_json_str(), '{"test_time": {"$time": "12:12:12"}, "_id": "121212"}')
        self.assertEqual(doc2.as_json_str(), '{"test_time": {"$time": "12:12:12"}, "_id": "121212"}')
        self.assertEqual(doc3.as_json_str(), '{"test_time": {"$time": "12:12:12"}, "_id": "121212"}')

    def test_doc_set_timestamp(self):
        doc1 = OJAIDocument().set('test_timestamp', OTimestamp(millis_since_epoch=29877132000)).set_id('121212')
        doc2 = OJAIDocument().set('test_timestamp', OTimestamp(year=1970, month_of_year=12, day_of_month=12,
                                                               hour_of_day=12, minute_of_hour=12, second_of_minute=12,
                                                               millis_of_second=12)).set_id('121212')
        doc3 = OJAIDocument().set('test_timestamp', OTimestamp(date=datetime(year=1970, month=12, day=12, hour=12,
                                                                             minute=12, second=12))).set_id('121212')
        self.assertEqual(doc1.as_json_str(), '{"test_timestamp": {"$date": "1970-12-12T19:12:12.000000Z"}, "_id": '
                                             '"121212"}')
        self.assertEqual(doc2.as_json_str(), '{"test_timestamp": {"$date": "1970-12-12T12:12:12.012000Z"}, "_id": '
                                             '"121212"}')
        self.assertEqual(doc3.as_json_str(), '{"test_timestamp": {"$date": "1970-12-12T12:12:12.000000Z"}, "_id": '
                                             '"121212"}')

    def test_doc_set_interval(self):
        doc = OJAIDocument() \
            .set('test_interval', OInterval(milli_seconds=172800000))
        self.assertEqual(doc.as_json_str(), '{"test_interval": {"$interval": 172800000}}')
        doc.set_id('121212') \
            .set('test_int', 123) \
            .set('test_timestamp', OTimestamp(millis_since_epoch=29877132000)) \
            .set('test_float', 11.1)
        self.assertEqual(doc.as_json_str(), '{"test_interval": {"$interval": 172800000}, "test_float": {'
                                            '"$numberFloat": 11.1}, "_id": "121212", "test_int": {"$numberLong": '
                                            '123}, "test_timestamp": {"$date": "1970-12-12T19:12:12.000000Z"}}')

    def test_doc_set_int(self):
        doc = OJAIDocument().set('test_int', 123).set_id('121212')
        self.assertEqual(doc.as_json_str(), '{"_id": "121212", "test_int": {"$numberLong": 123}}')

    def test_doc_set_bool(self):
        doc = OJAIDocument() \
            .set('test_bool', True) \
            .set('test_boolean_false', False)
        self.assertEqual(doc.as_json_str(), '{"test_bool": true, "test_boolean_false": false}')
        doc.set('test_int', 11) \
            .set('test_long', long(123))
        self.assertEqual(doc.as_json_str(), '{"test_bool": true, "test_long": {"$numberLong": 123}, "test_int": {'
                                            '"$numberLong": 11}, "test_boolean_false": false}')

    def test_doc_set_decimal(self):
        doc = OJAIDocument().set('test_decimal', Decimal(3.14))
        self.assertEqual(doc.as_json_str(),
                         '{"test_decimal": {"$decimal": "3.140000000000000124344978758017532527446746826171875"}}')

    def test_doc_set_float(self):
        doc = OJAIDocument() \
            .set('test_float', 11.1) \
            .set('test_float_two', 12.34)
        self.assertEqual(doc.as_json_str(), '{"test_float": {"$numberFloat": 11.1}, "test_float_two": {'
                                            '"$numberFloat": 12.34}}')
        doc.set('test_int', 999).set('test_long', long(51233123))
        self.assertEqual(doc.as_json_str(), '{"test_float": {"$numberFloat": 11.1}, "test_long": {"$numberLong": '
                                            '51233123}, "test_float_two": {"$numberFloat": 12.34}, "test_int": {'
                                            '"$numberLong": 999}}')
        doc.set('test_bool', False)
        self.assertEqual(doc.as_json_str(), '{"test_float": {"$numberFloat": 11.1}, "test_bool": false, '
                                            '"test_long": {"$numberLong": 51233123}, "test_int": {"$numberLong": '
                                            '999}, "test_float_two": {"$numberFloat": 12.34}}')

    def test_doc_set_dict(self):
        test_dict = {'field_one': 12, 'field_two': 14}
        doc = OJAIDocument().set('test_dict', test_dict)
        self.assertEqual(doc.as_json_str(), '{"test_dict": {"field_one": {"$numberLong": 12}, "field_two": {'
                                            '"$numberLong": 14}}}')
        doc.set_id('50')
        self.assertEqual(doc.as_json_str(), '{"_id": "50", "test_dict": {"field_one": {"$numberLong": 12}, '
                                            '"field_two": {"$numberLong": 14}}}')
        doc.set('test_dict.insert', 90)
        self.assertEqual(doc.as_json_str(), '{"_id": "50", "test_dict": {"field_one": {"$numberLong": 12}, '
                                            '"insert": {"$numberLong": 90}, "field_two": {"$numberLong": 14}}}')

    def test_doc_set_byte_array(self):
        byte_array = bytearray([0x13, 0x00, 0x00, 0x00, 0x08, 0x00])
        doc = OJAIDocument().set('test_byte_array', byte_array)
        self.assertEqual(doc.as_json_str(),
                         '{"test_byte_array": {"$binary": "\\u0013\\u0000\\u0000\\u0000\\b\\u0000"}}')

    def test_doc_set_doc(self):
        doc_to_set = OJAIDocument().set_id('121212') \
            .set('test_int', 123) \
            .set('test_timestamp', OTimestamp(millis_since_epoch=29877132000)) \
            .set('test_float', 11.1)

        doc = OJAIDocument().set('test_int_again', 55).set('internal_doc', doc_to_set)
        self.assertEqual(doc.as_json_str(), '{"internal_doc": {"test_float": {"$numberFloat": 11.1}, "_id": "121212", '
                                            '"test_int": {"$numberLong": 123}, "test_timestamp": {"$date": '
                                            '"1970-12-12T19:12:12.000000Z"}}, "test_int_again": {"$numberLong": 55}}')

    def test_doc_set_none(self):
        doc = OJAIDocument().set('test_none', None)
        self.assertEqual('{"test_none": null}', doc.as_json_str())

    def test_doc_delete_first_level(self):
        doc = OJAIDocument().set_id('121212') \
            .set('test_int', 123) \
            .set('test_timestamp', OTimestamp(millis_since_epoch=29877132000)) \
            .set('test_float', 11.1)
        self.assertEqual(doc.as_json_str(), '{"test_float": {"$numberFloat": 11.1}, "_id": "121212", "test_int": {'
                                            '"$numberLong": 123}, "test_timestamp": {"$date": '
                                            '"1970-12-12T19:12:12.000000Z"}}')
        doc.delete('test_timestamp')
        self.assertEqual(doc.as_json_str(), '{"test_float": {"$numberFloat": 11.1}, "_id": "121212", "test_int": {'
                                            '"$numberLong": 123}}')

    def test_doc_delete_nested(self):
        doc = OJAIDocument().set_id('121212') \
            .set('test_int', 123) \
            .set('first.test_int', 1235) \
            .set('first.test_timestamp', OTimestamp(millis_since_epoch=29877132000)) \
            .set('test_float', 11.1)

        self.assertEqual(doc.as_json_str(), '{"test_float": {"$numberFloat": 11.1}, "_id": "121212", "test_int": {'
                                            '"$numberLong": 123}, "first": {"test_timestamp": {"$date": '
                                            '"1970-12-12T19:12:12.000000Z"}, "test_int": {"$numberLong": 1235}}}')

        doc.delete('first.test_int')
        self.assertEqual(doc.as_json_str(), '{"test_float": {"$numberFloat": 11.1}, "_id": "121212", "test_int": {'
                                            '"$numberLong": 123}, "first": {"test_timestamp": {"$date": '
                                            '"1970-12-12T19:12:12.000000Z"}}}')
        doc.delete('first.test_timestamp')
        self.assertEqual(doc.as_json_str(), '{"test_float": {"$numberFloat": 11.1}, "_id": "121212", "test_int": {'
                                            '"$numberLong": 123}, "first": {}}')

    def test_doc_set_list(self):
        nested_doc = OJAIDocument().set('nested_int', 11).set('nested_str', 'strstr')
        doc = OJAIDocument().set('test_list', [1, 2, 3, 4, False, 'mystr', [{}, {}, [7, 8, 9, nested_doc]]])
        self.assertEqual(doc.as_json_str(), '{"test_list": [{"$numberLong": 1}, {"$numberLong": 2}, {"$numberLong": '
                                            '3}, {"$numberLong": 4}, false, "mystr", [{}, {}, [{"$numberLong": 7}, '
                                            '{"$numberLong": 8}, {"$numberLong": 9}, {"nested_str": "strstr"}, '
                                            '{"nested_int": {"$numberLong": 11}}]]]}')

    # MAPRDB-779
    def test_document_change_value_type(self):
        doc = OJAIDocument().set_id('121212') \
            .set('test_int', 123) \
            .set('test_float', 11.1)
        self.assertEqual(doc.as_json_str(), '{"test_float": {"$numberFloat": 11.1}, "_id": "121212", "test_int": {'
                                            '"$numberLong": 123}}')
        doc.set('test_int', OTimestamp(millis_since_epoch=29877132000))

        self.assertEqual(doc.as_json_str(), '{"test_float": {"$numberFloat": 11.1}, "_id": "121212", "test_int": {'
                                            '"$date": "1970-12-12T19:12:12.000000Z"}}')

    def test_set_dict_instead_of_dict(self):
        doc = OJAIDocument()
        field = 'dict_field'
        doc.set(field, value={'n': 2})
        doc.set(field, value={'r': 3})
        self.assertEqual(json.loads(doc.as_json_str()), {field: {'r': {'$numberLong': 3}}})

    def test_set_list_instead_of_list(self):
        doc = OJAIDocument()
        field = 'list_field'
        doc.set(field, value=[1, 1])
        self.assertEqual(doc.as_json_str(), '{"list_field": [{"$numberLong": 1}, {"$numberLong": 1}]}')
        doc.set(field, value=[2, 2])
        self.assertEqual(doc.as_json_str(), '{"list_field": [{"$numberLong": 2}, {"$numberLong": 2}]}')

    def test_set_decimal(self):
        doc = OJAIDocument().set('test_decimal', Decimal(3.14))
        self.assertEqual(doc.as_dictionary(),
                         {u'test_decimal': Decimal('3.140000000000000124344978758017532527446746826171875')})
        self.assertEqual(doc.as_json_str(),
                         '{"test_decimal": {"$decimal": "3.140000000000000124344978758017532527446746826171875"}}')
        from mapr.ojai.ojai.OJAIDocumentCreator import OJAIDocumentCreator
        parsed_doc = OJAIDocumentCreator.create_document(doc.as_json_str())
        self.assertEqual(parsed_doc.as_dictionary(),
                         {u'test_decimal': Decimal('3.140000000000000124344978758017532527446746826171875')})
        self.assertEqual(parsed_doc.as_json_str(),
                         '{"test_decimal": {"$decimal": "3.140000000000000124344978758017532527446746826171875"}}')