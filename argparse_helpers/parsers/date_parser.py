from datetime import datetime


def date_parser(s):
    return datetime.strptime(s, '%Y-%m-%d').date()
