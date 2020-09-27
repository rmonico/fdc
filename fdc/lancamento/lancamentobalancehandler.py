from commons.tableprinter import TablePrinter
from di_container.injector import Inject
from decimal import Decimal
from collections import OrderedDict


class LancamentoBalanceHandler(object):

    def __init__(self):
        self._lancamento_dao = Inject('lancamento dao')

    def lancamento_balance_command_handler(self, args):
        # TODO Limit this by date
        lancamentos_to_work_on = self._lancamento_dao.list_with_contas()
    
        lancamentos_per_day = self._group_lancamentos_per_day(lancamentos_to_work_on)

        saldos = dict()

        saldos_do_dia = dict()

        for data, lancamentos in lancamentos_per_day.items():
            for lancamento in lancamentos:
                self._update_balance(saldos_do_dia, lancamento.origem, -lancamento.valor)
                self._update_balance(saldos_do_dia, lancamento.destino, lancamento.valor)

            saldos[data] = saldos_do_dia

        return 'ok', {'saldos': saldos}

    def _group_lancamentos_per_day(self, lancamentos):
        lancamentos_per_day = {}

        for lancamento in lancamentos:
            day_lancamentos = lancamentos_per_day.setdefault(lancamento.data, [])

            day_lancamentos.append(lancamento)

        return lancamentos_per_day

    def _update_balance(self, saldos_do_dia, conta, valor):
        if 'contabilizável' in conta.propriedades:
            saldo = saldos_do_dia.setdefault(conta.nome, Decimal(0))

            saldo += Decimal(valor) / Decimal(100)

            saldos_do_dia[conta.nome] = saldo


