class DatabaseRestoreCommand(object):

    def database_parser_created_handler(self, db_parser):
        db_parser.add_parser("restore", help="Restore fdc.dump to fdc.db").set_defaults(
            event='database_restore_command')

    def database_restore_command_handler(self, args):
        print('TODO')

        return 'ok'
