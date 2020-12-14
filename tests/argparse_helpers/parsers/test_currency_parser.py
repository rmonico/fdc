from unittest import TestCase
from argparse_helpers.parsers.currency_parser import currency_parser
from decimal import Decimal


class CurrencyParserTestCase(TestCase):
    def test_single_value_should_parse_to_decimal(self):
        parsed = currency_parser('17.99')

        self.assertEqual(type(parsed), Decimal)
        self.assertEqual(parsed, Decimal('17.99'))
