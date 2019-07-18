#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sqlite3

from di_container.injector import Inject


class ConnectionFactory(object):

    def __init__(self):
        self._configs = Inject('app configuration')

    @staticmethod
    def get_external_resources():
        return [{'name': 'database connection', 'creator': ConnectionFactory.create_connection}]

    def create_connection(self):
        import os

        os.makedirs(self._configs['db']['folder'], exist_ok=True)

        return sqlite3.connect(self._configs['db']['path'])
