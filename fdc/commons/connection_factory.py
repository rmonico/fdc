import sqlite3

from di_container.injector import Inject


class ConnectionFactory(object):

    def __init__(self):
        self._configs = Inject('app configuration')
        self._logger = Inject('logger')

    @staticmethod
    def get_external_resources():
        return [{'name': 'database connection', 'creator': ConnectionFactory.create_connection}]

    def create_connection(self):
        import os

        connection = sqlite3.connect(self._configs['fdc.db_full_path'])

        self._logger.debug('Connected to database at {}', self._configs['fdc.db_full_path'])

        return connection
