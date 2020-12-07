from . base_command_test_case import BaseCommandTestCase


class ContaCommandsTests(BaseCommandTestCase):

    def setUp(self):
        super().setUp()
        self._call_fdc('db', 'init')

    def test_conta_add_should_create_new_conta(self):
        self._call_fdc('conta', 'add', 'conta_teste')

        with self.runsql('select rowid, nome from conta;') as rs:
            self.assertResultSet(rs, (1, 'conta_teste'))

    def test_conta_list_should_list_contas(self):
        self._call_fdc('conta', 'add', 'conta_1')
        self._call_fdc('conta', 'add', 'conta_2')

        stdout = self._call_fdc('conta', 'list')

        self.assertWithFile(stdout, __file__, 'expected_conta_list')


if __name__ == '__main__':
    unittest.main()
