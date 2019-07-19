class DatabaseDumpCommand(object):

    def database_parser_created_handler(self, db_parser):
        db_parser.add_parser("dump", help="Dump fdc.db to fdc.dump").set_defaults(event='database_dump_command')

    def database_dump_command_handler(self, args):
        print('TODO')

        return 'ok'
