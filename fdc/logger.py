#!/usr/bin/env python3
# -*- coding: utf-8 -*-


_INFO = 1


class Logger(object):

    def __init__(self):
        self._verbosity_level = _INFO

    def injectable_resource():
        return 'logger'

    def info(self, message, *args, **kwargs):
        if self._verbosity_level >= _INFO:
            print(message.format(args, **kwargs))
