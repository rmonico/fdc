from unittest import TestCase
from argparse_helpers.parsers.date_parser import date_parser
from datetime import date


class DateParserTestCase(TestCase):
    def test_single_value_should_parse_to_date(self):
        parsed = date_parser('2020-11-01')

        self.assertEqual(type(parsed), date)
        self.assertEqual(parsed.year, 2020)
        self.assertEqual(parsed.month, 11)
        self.assertEqual(parsed.day, 1)
