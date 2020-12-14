from tests.highlevel_command_testcase import HighLevelCommandTestCase


class LancCommandsTests(HighLevelCommandTestCase):

    def test_lanc_list_should_list_lancs(self):
        self._call_fdc('conta', 'add', 'conta_origem')
        self._call_fdc('conta', 'add', 'conta_destino')

        self._call_fdc('lanc', 'add', 'conta_origem', 'conta_destino', '31.99')

        stdout = self._call_fdc('lanc', 'list')

        self.assertWithRegexFile(stdout, __file__, 'expected_lanc_list')


if __name__ == '__main__':
    unittest.main()
