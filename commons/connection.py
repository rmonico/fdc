#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sqlite3


class Configurations(object):

    def __init__(self):
        self._logger = None

    @staticmethod
    def get_external_resources():
        return [{'name': 'configs', 'creator': Configurations._load_configurations}]

    def set_logger(self, logger):
        self._logger = logger

    def _visit_configs(self, visitor):
        self._visit_config(None, self._configs, visitor)

    def _visit_config(self, parent_key, configs, visitor):
        for key, value in configs.items():
            if parent_key:
                qualified_key = parent_key + '.' + key
            else:
                qualified_key = key

            if isinstance(value, dict):
                self._visit_config(qualified_key, value, visitor)
            else:
                visitor(qualified_key, value)

    def _load_configurations(self):
        # TODO Load this from file
        import os

        db_folder = '{HOME}/.config/fdc'.format(**os.environ)
        db_path = '{}/database.db'.format(db_folder)

        self._configs = {'db': {'folder': db_folder, 'path': db_path}}

        self._logger.info('Loaded configs:')

        self._visit_configs(lambda key, value: self._logger.info('  {}={}'.format(key, value)))

        return self._configs


class ConnectionFactory(object):

    def __init__(self):
        self._configs = None

    @staticmethod
    def get_external_resources():
        return [{'name': 'connection', 'creator': ConnectionFactory.create_connection}]

    def set_configs(self, configs):
        self._configs = configs

    def create_connection(self):
        import os

        os.makedirs(self._configs['db']['folder'], exist_ok=True)

        return sqlite3.connect(self._configs['db']['path'])
