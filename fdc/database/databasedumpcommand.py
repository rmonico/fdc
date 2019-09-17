from di_container.injector import Inject


class DatabaseDumpCommand(object):

    def __init__(self):
        self._logger = Inject('logger')
        self._connection = Inject('database connection')
        self._config = Inject('app configuration')

    def database_parser_created_handler(self, db_parser):
        db_parser.add_parser("dump", help="Dump database.db to database.dump").set_defaults(
            event='database_dump_command')

    def database_dump_command_handler(self, args):
        with open(self._config['fdc.dump_full_path'], 'w') as file:
            for line in self._connection.iterdump():
                file.write('%s\n' % line)

        return 'ok'

    def database_dump_command_ok_handler(self):
        print('Database contents dumped')
