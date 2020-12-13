from . base_command_test_case import BaseCommandTestCase
from unittest import skip

class LancCommandsTests(BaseCommandTestCase):

    def setUp(self):
        super().setUp()
        self._call_fdc('db', 'init')

    # def test_lanc_add_should_create_new_conta(self):
    #     self._call_fdc('conta', 'add', 'conta_teste')

    #     with self.runsql('select rowid, nome from conta;') as rs:
    #         self.assertResultSet(rs, (1, 'conta_teste'))

    @skip
    def test_lanc_list_should_list_lancs(self):
        self._call_fdc('conta', 'add', 'conta_origem')
        self._call_fdc('conta', 'add', 'conta_destino')

        self._call_fdc('lanc', 'add', 'conta_origem', 'conta_destino', '31.99')

        stdout = self._call_fdc('lanc', 'list')

        # Problema: a data é variável
        # Ideia: substituir com variáveis de ambiente no generator
        self.assertWithFile(stdout, __file__, 'expected_lanc_list')


if __name__ == '__main__':
    unittest.main()
