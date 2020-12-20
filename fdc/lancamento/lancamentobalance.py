from decimal import Decimal

from commons.tableprinter import TablePrinterFactory, Column
from converters import currency


class LancamentoBalance(object):

    def lancamento_parser_created_handler(self, lancamento_parser):
        parser = lancamento_parser.add_parser('balance', help='Lists the balance evolution day by day')

        parser.set_defaults(event='lancamento_balance_command')

    def lancamento_balance_command_ok_handler(self, saldos, contas):
        factory = TablePrinterFactory()

        factory.date_column().of_attr('data').add()

        for conta in contas:
            factory.add(_ContaColumn(conta))

        factory.add(_TotalColumn(contas))

        printer = factory.create()

        printer.print(saldos)


class _ContaColumn(Column):

    def __init__(self, conta):
        super().__init__(conta, self._getter, currency.formatter)

    def _getter(self, row, data):
        return data[row].get(self.title, None)


class _TotalColumn(Column):

    def __init__(self, contas):
        super().__init__('Total', self._getter, currency.formatter)
        self._contas = contas

    def _getter(self, row, data):
        total = Decimal(0)

        for conta in self._contas:
            if conta in data[row]:
                total += data[row].get(conta)

        return total
