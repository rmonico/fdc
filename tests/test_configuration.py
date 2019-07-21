from unittest import TestCase

from commons.configurations import Configurations


class TestConfiguration(TestCase):

    def test_get(self):
        c = Configurations({'key': 'value'})

        self.assertEqual(c.get('key'), 'value')
