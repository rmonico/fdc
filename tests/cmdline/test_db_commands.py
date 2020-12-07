from . base_command_test_case import BaseCommandTestCase
import sqlite3
import os


class DBCommandsTestCase(BaseCommandTestCase):

    def test_db_init(self):
        self._call_fdc('db', 'init')

        database_filename = self._env('FDC_FOLDER') + '/main.db'

        self.assertTrue(os.path.exists(self._env('FDCRC')))
        self.assertTrue(os.path.exists(database_filename))

        # TODO Check columns of every table
        self.assert_database_has_tables(database_filename, 'Conta', 'Cotacao', 'Orcamento', 'OrcamentoLancamento', 'Lancamento', 'Produto', 'Fornecedor')

    def test_db_restore(self):
        file = open(self._env('FDC_FOLDER') + '/main.dump', 'w')

        file.write('create table test(column)')

        file.close()

        self._call_fdc('db', 'restore')

        database_filename = self._env('FDC_FOLDER') + '/main.db'

        self.assertTrue(os.path.exists(database_filename))

        self.assert_database_has_tables(database_filename, 'test')

    def test_db_dump_should_dump_database_contents_on_file(self):
        database_filename = self._env('FDC_FOLDER') + '/main.db'

        with sqlite3.connect(database_filename) as connection:
            connection.executescript("create table test(column);")

        self._call_fdc('db', 'dump')

        with open(self._env('FDC_FOLDER') + '/main.dump', 'r') as dump_file:
            self.assertWithFile(dump_file, __file__, 'expected_dump_test')

    # def test_db_dump_should_create_new_commit_with_dump_file(self):
    #     pass


if __name__ == '__main__':
    unittest.main()
