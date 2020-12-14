from datetime import datetime
import re
from argparse import ArgumentTypeError


_format = '%Y-%m-%d'

def parse(s):
    if not re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', s):
        raise ArgumentTypeError('Invalid date value: "{}" (should be in format YYYY-MM-DD)'.format(s))

    return datetime.strptime(s, _format).date()


def format(value):
    return value.strftime(_format)
