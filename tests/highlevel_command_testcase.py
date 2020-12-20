from tests.base_command_test_case import BaseCommandTestCase


class HighLevelCommandTestCase(BaseCommandTestCase):

    def setUp(self):
        super().setUp()
        self._call_fdc('db', 'init')
