from unittest import TestCase
from converters import currency
from decimal import Decimal
from argparse import ArgumentTypeError


class CurrencyParserTestCase(TestCase):

    def test_single_value_should_parse_to_decimal(self):
        parsed = currency.parse('17.99')

        self.assertEqual(type(parsed), Decimal)
        self.assertEqual(parsed, Decimal('17.99'))

    def test_invalid_value_should_raise_exception(self):
        with self.assertRaises(ArgumentTypeError):
          currency.parse('invalid value')

