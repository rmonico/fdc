#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from datetime import date, datetime


def date_parser(s):
    return datetime.strptime(s, '%Y-%m-%d')
