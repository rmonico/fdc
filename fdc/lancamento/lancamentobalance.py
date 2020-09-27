from commons.tableprinter import TablePrinter
from types import SimpleNamespace
from decimal import Decimal


class LancamentoBalance(object):

    def lancamento_parser_created_handler(self, lancamento_parser):
        parser = lancamento_parser.add_parser('balance', help='Lists the balance evolution day by day')

        parser.set_defaults(event='lancamento_balance_command')


    def lancamento_balance_command_ok_handler(self, saldos, contas):
        printer = TablePrinter(['Data'] + contas + ['Total'], saldos, _SaldoDataProvider(contas))

        printer.print()


class _SaldoDataProvider(object):

    def __init__(self, contas):
        self._contas = contas

    def get_value(self, row, field, result_set):
        if field == 'Data':
            return row
        elif field == 'Total':
            total = Decimal(0)

            for conta in self._contas:
                if conta in result_set[row]:
                    total += result_set[row].get(conta)

            return total
        else:
            return result_set[row].get(field)

