class LancamentoAddCommand(object):

    @staticmethod
    def lancamento_parser_created_handler(lancamento_parser):
        lancamento_add_parser = lancamento_parser.add_parser('add', aliases=['a'],
                                                             help='Adiciona um novo lançamento')

        lancamento_add_parser.set_defaults(event='lancamento_add_command')

    def lancamento_add_command_handler(self, args):
        return 'ok'

    def lancamento_add_command_ok_handler(self):
        print('TODO')
