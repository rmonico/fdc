from decimal import Decimal

from di_container.injector import Inject


class LancamentoBalanceHandler(object):

    def __init__(self):
        self._lancamento_dao = Inject('lancamento dao')

    def lancamento_balance_command_handler(self, args):
        # TODO Limit this by date
        lancamentos = self._lancamento_dao.list_with_contas()

        lancamentos_per_day = self._group_lancamentos_per_day(lancamentos)

        saldos = dict()
        balance = dict()

        for data, lancamentos in lancamentos_per_day.items():
            for lancamento in lancamentos:
                self._update_balance(balance, lancamento.origem, -lancamento.valor)

                self._update_balance(balance, lancamento.destino, lancamento.valor)

            saldos[data] = dict(balance)

        contas = list(set(balance.keys()))

        contas.sort()

        return 'ok', {'saldos': saldos, 'contas': contas}

    def _group_lancamentos_per_day(self, lancamentos):
        lancamentos_per_day = {}

        for lancamento in lancamentos:
            day_lancamentos = lancamentos_per_day.setdefault(lancamento.data, [])

            day_lancamentos.append(lancamento)

        return lancamentos_per_day

    def _update_balance(self, diario, conta, valor):
        if 'contabilizável' in conta.propriedades:
            saldo = diario.setdefault(conta.nome, Decimal(0))

            saldo += Decimal(valor) / Decimal(100)

            diario[conta.nome] = saldo
