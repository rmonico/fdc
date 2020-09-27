class LancamentoBalance(object):

    def lancamento_parser_created_handler(self, lancamento_parser):
        parser = lancamento_parser.add_parser('balance', help='Lists the balance evolution day by day')

        parser.set_defaults(event='lancamento_balance_command')


    def lancamento_balance_command_ok_handler(self, saldos):
        # printer = TablePrinter(self._lancamento_dao._metadata.fields, saldos)

        # printer.print()

        for data, saldo in sorted(saldos.items()):
            print('{} - {}'.format(data, saldo))

