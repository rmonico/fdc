from commons.tableprinter import TablePrinterFactory
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
        lancamentos = self._dao.list_with_contas()

        return 'ok', {'lancamentos': lancamentos}

    def lancamento_list_command_ok_handler(self, lancamentos):
        factory = TablePrinterFactory()

        factory.date_column().of_attr('data').add()
        factory.string_column().of_attr('origem.nome').add()
        factory.string_column().of_attr('destino.nome').add()
        factory.currency_column().of_attr('valor').add()
        factory.string_column().of_attr('observacao').title('Observação').add()

        printer = factory.create()

        printer.print(lancamentos)
