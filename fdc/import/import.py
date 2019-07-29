from di_container.controller import controller


class ImportCommand(object):

    def root_parser_created_handler(self, root_parser):
        import_parser = root_parser.add_parser(
            "import", help="Import data from external source")
        subparsers = import_parser.add_subparsers()

        controller.event('import_parser_created', import_parser=subparsers)
