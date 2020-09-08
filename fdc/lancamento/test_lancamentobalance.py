from unittest import TestCase
from fdc.lancamento.lancamentobalance import LancamentoBalance


class LancamentoBalanceTests(TestCase):

    def setup(self):
        packages = ['commons', 'di_container', __package__ + '.commons', __package__ + '.conta',
                        __package__ + '.database', __package__ + '.import', 'fdc.lancamento', 'fdc.produto',
                        'fdc.fornecedor', ]
        di_container.load_resources(packages)
        di_container.inject_resources(self, profile='test')

        controller.load_listeners(packages)

    def test_lancamento_balance_command(self):
        command = LancamentoBalance()

        # Encontrar (ou fazer) um jeito de "Inject('lancamento dao')" retornar uma classe que devolva uma lista customizada de lancamentos
        result = command.lancamento_balance_command_handler(None)

        self.assertTrue(result[0], 'ok')
        self.assertTrue(result[1].keys(), ['saldos'])
        self.assertTrue(result[1].values() is list)

