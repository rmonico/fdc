from di_container.controller import controller


class LancamentoCommand(object):

    @staticmethod
    def root_parser_created_handler(root_parser):
        lancamento_parser = root_parser.add_parser('lanc', aliases=['la'], help='Lançamento commands')
        subparsers = lancamento_parser.add_subparsers()

        controller.event('lancamento_parser_created', lancamento_parser=subparsers)
