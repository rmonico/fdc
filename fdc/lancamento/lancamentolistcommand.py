class LancamentoListCommand(object):

    def __init__(self):
      pass

    def lancamento_parser_created_handler(self, lancamento_parser):
      parser = lancamento_parser.add_parser('list', aliases=['ls'], help='Lista os lançamentos existentes')

      parser.set_defaults(event='lancamento_list_command')

      # TODO
      # parser.add_argument('filter')

    def lancamento_list_command_handler(self, args):
      # Business rule
      return 'ok'

    def lancamento_list_command_ok_handler(self):
      print('OK')
