from commons.tableprinter import TablePrinter
from di_container.injector import Inject


class LancamentoListCommand(object):

    def __init__(self):
      self._dao = Inject('lancamento dao')

    def lancamento_parser_created_handler(self, lancamento_parser):
      parser = lancamento_parser.add_parser('list', aliases=['ls'], help='Lista os lançamentos existentes')

      parser.set_defaults(event='lancamento_list_command')

      # TODO
      # parser.add_argument('-f', '--filter', type=str, help='Filter to be applied')
      # parser.add_argument('-b', '--balance', action='store_true', help='Calculate the balances for each line')


    def lancamento_list_command_handler(self, args):
      lancamentos = self._dao.list()

      return 'ok', {'lancamentos': lancamentos}

    def lancamento_list_command_ok_handler(self, lancamentos):
      printer = TablePrinter(self._dao._metadata.fields, lancamentos)

      printer.print()
