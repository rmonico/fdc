from decimal import Decimal
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import MagicMock

from fdc.lancamento.lancamentobalancehandler import LancamentoBalanceHandler


class LancamentoBalanceTests(TestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)

        self._contas = list()

        self._conta('itau', 'contabilizável')
        self._conta('carteira', 'contabilizável')
        self._conta('lanche')
        self._conta('casa')

    def _conta(self, nome, propriedades=''):
        conta = SimpleNamespace(nome=nome, propriedades=propriedades)

        self._contas.append(conta)

    def setUp(self):
        self._lancamentos = list()

        self._command = LancamentoBalanceHandler()

        self._command._lancamento_dao.list_with_contas = MagicMock(return_value=self._lancamentos)

    def test_should_lancamento_balance_return_balances(self):
        self._lancamento('2020-09-01', 'itau', 'carteira', 150.00)
        self._lancamento('2020-09-01', 'carteira', 'lanche', 5.00)
        self._lancamento('2020-09-01', 'carteira', 'casa', 50.00)

        result = self._command.lancamento_balance_command_handler(None)

        saldos = self.assertResult(result, status='ok')

        diario = self.assertHasData(saldos, '2020-09-01')
        self.assertBalanceIs(diario, 'itau', -150)
        self.assertBalanceIs(diario, 'carteira', 95)

    def test_should_lancamento_balance_accumulate_throught_the_days(self):
        self._lancamento('2020-09-01', 'itau', 'carteira', 150.00)
        self._lancamento('2020-09-01', 'carteira', 'lanche', 5.00)
        self._lancamento('2020-09-01', 'carteira', 'casa', 50.00)

        self._lancamento('2020-09-02', 'carteira', 'itau', 50.00)

        result = self._command.lancamento_balance_command_handler(None)

        saldos = self.assertResult(result, status='ok')

        diario = self.assertHasData(saldos, '2020-09-01')
        self.assertBalanceIs(diario, 'itau', -150)
        self.assertBalanceIs(diario, 'carteira', 95)

        diario = self.assertHasData(saldos, '2020-09-02')
        self.assertBalanceIs(diario, 'itau', -100)
        self.assertBalanceIs(diario, 'carteira', 45)

    def assertResult(self, result, status):
        self.assertEqual(result[0], status)
        self.assertTrue('saldos' in result[1])
        saldos = result[1]['saldos']
        self.assertIsInstance(saldos, dict)

        return saldos

    def assertHasData(self, saldos, data):
        self.assertTrue(data in saldos.keys())
        return saldos[data]

    def assertBalanceIs(self, saldos, nome_conta, saldo):
        self.assertTrue(nome_conta in saldos)
        self.assertEqual(saldos[nome_conta], Decimal(saldo))

    def _lancamento(self, data, nome_origem, nome_destino, valor):
        origem = self._conta_by_nome(nome_origem)
        destino = self._conta_by_nome(nome_destino)

        # FIXME "valor" is being multiplied by 100 due to a bug on database saving
        lancamento = SimpleNamespace(data=data, origem=origem, destino=destino, valor=valor * 100)

        self._lancamentos.append(lancamento)

    def _conta_by_nome(self, conta_nome):
        for conta in self._contas:
            if conta.nome == conta_nome:
                return conta

        raise Exception('Conta não encontrada: {}'.format(conta_nome))
