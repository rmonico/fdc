from datetime import datetime


def parse(s):
    return datetime.strptime(s, '%Y-%m-%d').date()
