#!/usr/bin/env python3
# -*- coding: utf-8 -*-


_INFO = 1
_verbosity_level = _INFO


def info(message, parameters=None):
    if _verbosity_level >= _INFO:
        print("{}: '{}'".format(message, parameters))
