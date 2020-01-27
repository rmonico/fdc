import argparse
import decimal
import re


def currency_parser(s):
    if not re.match('^[0-9]+\.[0-9]{2}$', s):
        raise argparse.ArgumentTypeError('Invalid currency value: "{}" (should be in format 0.00)'.format(s))

    return decimal.Decimal(s)
