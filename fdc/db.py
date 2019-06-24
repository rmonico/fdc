#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Init(object):

    def run(self, args):
        print("in db init {}".format(args))


class Restore(object):

    def run(self, args):
        # Usar iterdump do sqlite3
        pass