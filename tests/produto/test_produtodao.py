import unittest

from di_container.injector import di_container, Inject
from commons.sqlite_connection_factory import ConnectionFactory
from commons.logger import Logger
from tests.commons.test_configuration import TestConfiguration
from fdc.produto.produtodao import ProdutoDao


class ProdutoDaoTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        di_container.load_resources_from_class(TestConfiguration, Logger, ConnectionFactory, ProdutoDao)

        conn = di_container.get_resource('database connection')

        conn.executescript('create table Produto ('
                           '  nome text not null,'
                           '  medida text,'
                           '  unidade text);')

    def setUp(self):
        self._conn = di_container.get_resource('database connection')

        self.dao = di_container.get_resource('produto dao')

    def tearDown(self):
        self._conn.executescript('delete from produto;')

    def test_exists_with_name_only(self):
        self._conn.executescript('insert into produto (nome) values ("Café");')

        self.assertEqual(True, self.dao.exists('Café'))

    def test_exists_with_produto_with_medida_and_unidade(self):
        self._conn.executescript(
            'insert into produto (nome, medida, unidade) values ("Café", "100", "gramas");')

        self.assertEqual(True, self.dao.exists('Café 100 gramas'))


if __name__ == '__main__':
    unittest.main()
