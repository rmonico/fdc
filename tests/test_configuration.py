from unittest import TestCase

from commons.configurations import Configurations


class TestConfiguration(TestCase):

    def test_single_get(self):
        c = Configurations({'key': 'value'})

        self.assertEqual(c.get('key'), 'value')

    def test_get_with_subkeys(self):
        c = Configurations({'key': {'keys first subkey': 'subkey value', 'anothersubkey': 'another sub key value', 'subkey': {'first subsubkey': 'value of first sub sub key'}}})

        self.assertIsInstance(c.get('key'), dict)
        self.assertEqual(c.get('key.keys first subkey'), 'subkey value')
        self.assertEqual(c.get('key.anothersubkey'), 'another sub key value')
        self.assertIsInstance(c.get('key.subkey'), dict)
        self.assertEqual(c.get('key.subkey.first subsubkey'), 'value of first sub sub key')
