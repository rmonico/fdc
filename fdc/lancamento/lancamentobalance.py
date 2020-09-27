from commons.tableprinter import TablePrinter
from di_container.injector import Inject


class LancamentoBalance(object):

    def __init__(self):
      self._dao = Inject('lancamento dao')

    def lancamento_parser_created_handler(self, lancamento_parser):
      parser = lancamento_parser.add_parser('balance', help='Lists the balance evolution day by day')

      parser.set_defaults(event='lancamento_balance_command')

    def lancamento_balance_command_handler(self, args):
      # TODO Limit this by date
      lancamentos_to_work_on = self._dao.list()

      lancamentos_por_dia = self.group_lancamentos_per_day(lancamentos_to_work_on)

      saldos = {}

      for data, lancamentos in lancamentos_por_dia.items():
        saldo = {}
        for lancamento in lancamentos:
          saldo.ge

        saldos.set_default(data, saldo)

      return 'ok', {'saldos': saldos}

    def group_lancamentos_per_day(self, lancamentos):
      lancamentos_per_day = {}

      for lancamento in lancamentos:
        day_lancamentos = lancamentos_per_day.set_default(lancamento.data, [])

        day_lancamentos.append(lancamento)

      return lancamentos_per_day

    def lancamento_balance_command_ok_handler(self, saldos):
      printer = TablePrinter(self._dao._metadata.fields, saldos)

      printer.print()
