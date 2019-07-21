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

        os.makedirs(self._configs['db.folder'], exist_ok=True)

        connection = sqlite3.connect(self._configs['db.path'])

        self._logger.info('Connected to database at {}', self._configs['db.path'])

        return connection
