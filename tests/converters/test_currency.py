from argparse import ArgumentTypeError
from decimal import Decimal
from unittest import TestCase

from converters import currency


class CurrencyParserTestCase(TestCase):

    def test_single_value_should_parse_to_decimal(self):
        parsed = currency.parse('17.99')

        self.assertEqual(type(parsed), Decimal)
        self.assertEqual(parsed, Decimal('17.99'))

    def test_invalid_value_should_raise_exception(self):
        with self.assertRaises(ArgumentTypeError):
            currency.parse('invalid value')

    def test_negative_value_should_parse_to_decimal(self):
        parsed = currency.parse('-17.99')

        self.assertEqual(parsed, Decimal('-17.99'))

    def test_simple_value_should_format_it(self):
        formatted = currency.format(Decimal(17.99))

        self.assertEqual(formatted, '17.99')
