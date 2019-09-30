import decimal, re, argparse


def currency_parser(s):
    if not re.match('^[0-9]+\.[0-9]{2}$', s):
        raise argparse.ArgumentTypeError('Invalid currency: "{}"'.format(s))

    return decimal.Decimal(s)
