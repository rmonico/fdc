from argparse import ArgumentTypeError
from decimal import Decimal
import re


def parse(s):
    if not re.match('^-?[0-9]+\.[0-9]{2}$', s):
        raise ArgumentTypeError('Invalid currency value: "{}" (should be in format 0.00)'.format(s))

    return Decimal(s)

def format(value):
    return '{:.2f}'.format(value) if value != None else ''
