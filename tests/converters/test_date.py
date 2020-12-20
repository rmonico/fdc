from argparse import ArgumentTypeError
from datetime import datetime, date
from unittest import TestCase

from converters import date as date_converter


class DateParserTestCase(TestCase):

    def test_single_value_should_parse_to_date(self):
        parsed = date_converter.parse('2020-11-01')

        self.assertEqual(type(parsed), date)
        self.assertEqual(parsed.year, 2020)
        self.assertEqual(parsed.month, 11)
        self.assertEqual(parsed.day, 1)

    def test_invalid_value_should_raise_exception(self):
        with self.assertRaises(ArgumentTypeError):
            date_converter.parse('invalid value')

    def test_simple_value_should_format_it(self):
        date = datetime.strptime('2020-11-01', '%Y-%m-%d').date()

        formatted = date_converter.format(date)

        self.assertEqual(formatted, '2020-11-01')
