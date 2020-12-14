from tests.highlevel_command_testcase import HighLevelCommandTestCase
from datetime import date


class LancCommandsTests(HighLevelCommandTestCase):

    def test_lanc_list_should_list_lancs(self):
        self._call_fdc('conta', 'add', 'conta_origem')
        self._call_fdc('conta', 'add', 'conta_destino')

        self._call_fdc('lanc', 'add', 'conta_origem', 'conta_destino', '31.99')

        stdout = self._call_fdc('lanc', 'list')

        self.assertWithRegexFile(stdout, __file__, 'expected_lanc_list')

    def test_lanc_list_should_return_nothing_on_empty_list(self):
        stdout = self._call_fdc('lanc', 'list')

        self.assertWithRegexFile(stdout, __file__, 'expected_lanc_list_with_database_empty')

    def test_lanc_add_should_add_lanc_with_just_origem_destino_and_valor(self):
        self._call_fdc('conta', 'add', 'conta_origem')
        self._call_fdc('conta', 'add', 'conta_destino')

        self._call_fdc('lanc', 'add', 'conta_origem', 'conta_destino', '31.99')

        with self.runsql('select data, origem, destino, valor from lancamento;') as rs:
            self.assertResultSet(rs, (str(date.today()), 1, 2, 31.99))


if __name__ == '__main__':
    unittest.main()
