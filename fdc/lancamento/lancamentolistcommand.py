from commons.tableprinter import TablePrinter, Column, attr_column, format_currency
from di_container.injector import Inject
from decimal import Decimal


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
        printer = TablePrinter(lancamentos, [Column('Data', lambda lanc, d: lanc.data), _Column('Origem', lambda lanc, d: lanc.origem), _Column('Destino', lambda lanc, d: lanc.destino), _Column('Valor', lambda lanc, d: Decimal(lanc.valor) / Decimal(100), lambda v: '{:.2f}'.format(v)), _Column('Observação', lambda lanc, d: lanc.observacao)])

        printer.print()
