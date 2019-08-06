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
        # TODO Make this more generic, should not use fdc keys here!
        self._logger.debug('Connecting to database at {}...', self._configs['fdc.db_full_path'])

        connection = sqlite3.connect(self._configs['fdc.db_full_path'])

        return connection
