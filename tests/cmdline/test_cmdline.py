import os
import subprocess
from unittest import TestCase
import sqlite3
import shutil
from contextlib import contextmanager


class CommandLineTestCase(TestCase):

    def setUp(self):
        self._environment = os.environ.copy()

        self._env(
            'FDCRC', '{HOME}/.unittests_fdcrc'.format(**self._environment))
        self._env('FDC_FOLDER',
                  '{HOME}/.config/fdc_tests'.format(**self._environment))

        file = open(self._env('FDCRC'), 'w')

        file.write('fdc:\n')
        file.write('  folder: "{FDC_FOLDER}"\n')
        file.write('  db_file: "main.db"\n')
        file.write('  dump_file: "main.dump"\n')
        file.write('\n')
        file.write('log:\n')
        file.write('  verbosity: NONE\n')

        file.close()

        os.makedirs(self._env('FDC_FOLDER'), exist_ok=True)

    def _env(self, var, value=None):
        if value:
            self._environment[var] = value
        else:
            return self._environment[var]

    def tearDown(self):
        shutil.rmtree(self._env('FDC_FOLDER'))

        os.remove(self._env('FDCRC'))

    def _call_fdc(self, *args):
        return subprocess.run(['python', '-m', 'fdc.main'] + list(args), env=self._environment, stdout=subprocess.PIPE)

    @contextmanager
    def runsql(self, sql: str, database_file: str = None):
        if not database_file:
            database_file = self._env('FDC_FOLDER') + '/main.db'

        with sqlite3.connect(database_file) as connection:
            result_set = connection.execute(sql)

            try:
                yield result_set
            finally:
                result_set.close()

    def assert_database_has_tables(self, database_file: str, *tables: list):
        with self.runsql("select * from sqlite_master where type='table';", database_file) as result_set:
            table_count = 0

            for row in result_set:
                table = row[1]

                self.assertTrue(table in tables, '"{}" is not in table list'.format(table))

                table_count += 1

            self.assertEqual(table_count, len(tables), msg='Wrong table count')

    def test_db_init(self):
        result = self._call_fdc('db', 'init')

        self.assertEqual(result.returncode, 0)

        database_filename = self._env('FDC_FOLDER') + '/main.db'

        self.assertTrue(os.path.exists(self._env('FDCRC')))
        self.assertTrue(os.path.exists(database_filename))

        # TODO Check columns of every table
        self.assert_database_has_tables(database_filename, 'Conta', 'Cotacao', 'Orcamento', 'OrcamentoLancamento', 'Lancamento', 'Produto', 'Fornecedor')

    def test_db_restore(self):
        file = open(self._env('FDC_FOLDER') + '/main.dump', 'w')

        file.write('create table test(column)')

        file.close()

        result = self._call_fdc('db', 'restore')

        self.assertEqual(result.returncode, 0)

        database_filename = self._env('FDC_FOLDER') + '/main.db'

        self.assertTrue(os.path.exists(database_filename))

        self.assert_database_has_tables(database_filename, 'test')

    def test_db_dump_should_dump_database_contents_on_file(self):
        database_filename = self._env('FDC_FOLDER') + '/main.db'

        with sqlite3.connect(database_filename) as connection:
            connection.executescript("create table test(column);")

        result = self._call_fdc('db', 'dump')

        self.assertEqual(result.returncode, 0)

        with open(self._env('FDC_FOLDER') + '/main.dump', 'r') as dump_file:
            self.assertEqual(dump_file.readline(), 'BEGIN TRANSACTION;\n')
            self.assertEqual(dump_file.readline(), 'CREATE TABLE test(column);\n')
            self.assertEqual(dump_file.readline(), 'COMMIT;\n')

            dump_file.close()

    # def test_db_dump_should_create_new_commit_with_dump_file(self):
    #     pass

    def test_conta_add_should_create_new_conta(self):
        result = self._call_fdc('db', 'init').returncode

        if result != 0:
            self.fail('db init failed (returned {}), cant test conta add'.format(result))

        result = self._call_fdc('conta', 'add', 'conta_teste')

        self.assertEqual(result.returncode, 0)

        with self.runsql('select rowid, nome from conta;') as result_set:
            row = result_set.fetchone()

            self.assertEqual(row[0], 1)
            self.assertEqual(row[1], 'conta_teste')

            self.assertIsNone(result_set.fetchone())



if __name__ == '__main__':
    unittest.main()
