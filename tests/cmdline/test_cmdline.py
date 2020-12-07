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

    def _call_fdc(self, *args, **kwargs):
        process = subprocess.run(['python', '-m', 'fdc.main'] + list(args), env=self._environment, stdout=subprocess.PIPE)

        if process.returncode != 0:
            message = '{} failed (returned {})'.format(' '.join(args), process.returncode)

            if 'for_command' in kwargs:
                message += ', cant test {}'.format(kwargs['for_command'])

            self.fail(message)
        else:
            return process.stdout.decode().splitlines()

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
            self.assertEqual(dump_file.readline(), 'BEGIN TRANSACTION;\n')
            self.assertEqual(dump_file.readline(), 'CREATE TABLE test(column);\n')
            self.assertEqual(dump_file.readline(), 'COMMIT;\n')

    # def test_db_dump_should_create_new_commit_with_dump_file(self):
    #     pass

    def assertResultSet(self, result_set, *expected_tuples):
        for line, expected in enumerate(expected_tuples, start=1):
            self.assertTupleEqual(result_set.fetchone(), expected, msg='Line ' + str(line))

        self.assertIsNone(result_set.fetchone(), msg='Line ' + str(line))

    def test_conta_add_should_create_new_conta(self):
        self._call_fdc('db', 'init', for_command='conta add')

        self._call_fdc('conta', 'add', 'conta_teste')

        with self.runsql('select rowid, nome from conta;') as rs:
            self.assertResultSet(rs, (1, 'conta_teste'))

    def load_file(self, filename: str, module__file__):
        module_path = os.path.dirname(module__file__)

        file_path = os.path.join(module_path, filename)

        with open(file_path) as expected_file:
            return expected_file.read().splitlines()

    def assertWithFile(self, content: list, filename: str, msg=None):
        expected_lines = self.load_file('expected_conta_list', __file__)

        self.assertSequenceEqual(content, expected_lines, msg)

    def test_conta_list_should_list_contas(self):
        self._call_fdc('db', 'init', for_command='conta list')

        self._call_fdc('conta', 'add', 'conta_1', for_command='conta list')

        self._call_fdc('conta', 'add', 'conta_2', for_command='conta list')

        stdout = self._call_fdc('conta', 'list')

        self.assertWithFile(stdout, 'expected_conta_list')


if __name__ == '__main__':
    unittest.main()
