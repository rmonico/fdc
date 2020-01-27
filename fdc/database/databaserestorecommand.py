import os

from di_container.injector import Inject
from di_container.injector import di_container


class DatabaseRestoreCommand(object):

    def __init__(self):
        self._config = Inject('app configuration')
        self._logger = Inject('logger')
        self._git = Inject('fdc git wrapper')

    def database_parser_created_handler(self, db_parser):
        db_parser.add_parser("restore", help="Restore fdc.dump to fdc.db").set_defaults(
            event='database_restore_command')

        # TODO A flag to skip git pull
        # TODO A flag to rename existing database
        # TODO A parameter to change dump file location
        # TODO A parameter to change database to be restored
        # TODO A parameter to disable git pull

    def database_restore_command_handler(self, args):
        self._git.pull()

        # FIXME This will become huge after some time.....
        restore_database_script = self._get_database_restore_script()

        if not restore_database_script:
            return 'dump_file_not_found'

        connection = self._prepare_connection()

        # FIXME Rollback on error
        connection.executescript(restore_database_script)

        connection.commit()

        connection.close()

        return 'ok'

    def _get_database_restore_script(self):
        if not os.path.isfile(self._config['fdc.dump_full_path']):
            return None

        file = open(self._config['fdc.dump_full_path'], 'r')

        script = file.read()

        file.close

        return script

    def _prepare_connection(self):
        if os.path.isfile(self._config['fdc.db_full_path']):
            os.remove(self._config['fdc.db_full_path'])

        return di_container.get_resource('database connection')

    def database_restore_command_dump_file_not_found_handler(self):
        print('Dump file not found at "{}". Nothing to do.'.format(
            self._config['fdc.db_full_path']))

    def database_restore_command_ok_handler(self):
        print('Dump file at "{}" restored into database "{}" successfully.'.format(
            self._config['fdc.dump_full_path'], self._config['fdc.db_full_path']))
