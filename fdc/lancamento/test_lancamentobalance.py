from unittest import TestCase
from unittest.mock import MagicMock

from fdc.lancamento.lancamentobalancehandler import LancamentoBalanceHandler 
from types import SimpleNamespace
from argparse_helpers.parsers.date_parser import date_parser
from decimal import Decimal


class LancamentoBalanceTests(TestCase):

    def setUp(self):
        self._lancamentos = list()
        self._contas = list()

        self._command = LancamentoBalanceHandler()

        self._command._lancamento_dao.list_with_contas = MagicMock(return_value = self._lancamentos)


    def test_should_lancamento_balance_return_(self):
        self._conta('itau', 'contabilizável')
        self._conta('carteira', 'contabilizável')
        self._conta('lanche')
        self._conta('casa')

        self._lancamento('2020-09-01', 'itau', 'carteira', 150.00)
        self._lancamento('2020-09-01', 'carteira', 'lanche', 5.00)
        self._lancamento('2020-09-01', 'carteira', 'casa', 50.00)

        result = self._command.lancamento_balance_command_handler(None)

        self.assertEqual(result[0], 'ok')
        self.assertTrue('saldos' in result[1])
        saldos = result[1]['saldos']

        self.assertIsInstance(saldos, dict)
        self.assertTrue('2020-09-01' in saldos.keys())
        saldos_dia = saldos['2020-09-01']

        self.assertTrue('itau' in saldos_dia)
        self.assertEqual(saldos_dia['itau'], Decimal(-150.0))

        self.assertTrue('carteira' in saldos_dia)
        self.assertEqual(saldos_dia['carteira'], Decimal(95))


    def _lancamento(self, data, nome_origem, nome_destino, valor):
        origem = self._conta_by_nome(nome_origem)
        destino = self._conta_by_nome(nome_destino)

        lancamento = SimpleNamespace(data=data, origem=origem, destino=destino, valor=valor)

        self._lancamentos.append(lancamento)


    def _conta(self, nome, propriedades=''):
        conta = SimpleNamespace(nome=nome, propriedades=propriedades)

        self._contas.append(conta)


    def _conta_by_nome(self, conta_nome):
        for conta in self._contas:
            if conta.nome == conta_nome:
                return conta

        raise Exception('Conta não encontrada: {}'.format(conta_nome))

