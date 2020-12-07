from commons.tableprinter import TablePrinter, Column, format_currency
from types import SimpleNamespace
from decimal import Decimal


class LancamentoBalance(object):

    def lancamento_parser_created_handler(self, lancamento_parser):
        parser = lancamento_parser.add_parser('balance', help='Lists the balance evolution day by day')

        parser.set_defaults(event='lancamento_balance_command')


    def lancamento_balance_command_ok_handler(self, saldos, contas):
        columns = [Column('Data', lambda row, data: row)]

        for conta in contas:
            columns.append(_ContaColumn(conta))

        columns.append(_TotalColumn(contas))

        printer = TablePrinter(saldos, columns)

        printer.print()


class _ContaColumn(Column):

    def __init__(self, conta):
        super().__init__(conta, self._getter, _format_currency)

    def _getter(self, row, data):
        return data[row].get(self.title, None)


class _TotalColumn(Column):

    def __init__(self, contas):
        super().__init__('Total', self._getter, _format_currency)
        self._contas = contas

    def _getter(self, row, data):
        total = Decimal(0)

        for conta in self._contas:
            if conta in data[row]:
                total += data[row].get(conta)

        return total


def _format_currency(value):
    return '{:.2f}'.format(value) if value else ''
