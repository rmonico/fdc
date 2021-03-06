from di_container.controller import controller


class ContaCommand(object):

    def root_parser_created_handler(self, root_parser):
        conta_parser = root_parser.add_parser(
            "conta", aliases=['ct'], help="Comandos de conta")
        subparsers = conta_parser.add_subparsers()

        controller.event('conta_parser_created', conta_parser=subparsers)
