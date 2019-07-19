from di_container.controller import controller


class DBCommand(object):

    def root_parser_created_handler(self, root_parser):
        db_parser = root_parser.add_parser("db", help="Database commands")
        subparsers = db_parser.add_subparsers()

        controller.event('database_parser_created', db_parser=subparsers)
