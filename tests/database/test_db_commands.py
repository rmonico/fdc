import os

from tests.base_command_test_case import BaseCommandTestCase


class DBCommandsTestCase(BaseCommandTestCase):

    def assert_database_has_tables(self, *tables: list):
        with self.runsql("select * from sqlite_master where type='table';") as result_set:
            table_count = 0

            for row in result_set:
                table = row[1]

                self.assertTrue(table in tables, '"{}" is not in table list'.format(table))

                table_count += 1

            self.assertEqual(table_count, len(tables), msg='Wrong table count')

    def test_db_init(self):
        self._call_fdc('db', 'init')

        self.assertTrue(os.path.exists(self._env('FDCRC')))
        self.assertTrue(os.path.exists(self.get_db_file()))

        # TODO Check columns of every table
        self.assert_database_has_tables('Conta', 'Cotacao', 'Orcamento', 'OrcamentoLancamento', 'Lancamento', 'Produto',
                                        'Fornecedor')

    def test_db_restore(self):
        file = open(self._env('FDC_FOLDER') + '/main.dump', 'w')

        file.write('create table test(column)')

        file.close()

        self._call_fdc('db', 'restore')

        self.assertTrue(os.path.exists(self.get_db_file()))

        self.assert_database_has_tables('test')

    def test_db_dump_should_dump_database_contents_on_file(self):
        self.runscript('create table test(column);')

        self._call_fdc('db', 'dump')

        with open(self._env('FDC_FOLDER') + '/main.dump', 'r') as dump_file:
            self.assertWithLiteralFile(dump_file, __file__, 'expected_dump_test')

    # def test_db_dump_should_create_new_commit_with_dump_file(self):
    #     pass


if __name__ == '__main__':
    unittest.main()
