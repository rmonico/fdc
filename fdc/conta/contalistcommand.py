from di_container.injector import Inject
from commons.tableprinter import TablePrinter


class ContaListCommand(object):

    def __init__(self):
        self._dao = Inject('conta dao')

    @staticmethod
    def conta_parser_created_handler(conta_parser):
        conta_parser.add_parser("list", aliases=['l', 'ls'], help="Lista as contas existentes").set_defaults(
            event='conta_list_command')

    def conta_list_command_handler(self, args):
        contas = self._dao.list()

        return 'ok', contas

    def conta_list_command_ok_handler(self, contas):
        printer = TablePrinter(self._dao.fields(), contas)

        printer.print()
