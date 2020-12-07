import os
import subprocess
from unittest import TestCase
import sqlite3
import shutil
from contextlib import contextmanager
from collections.abc import Sequence


class BaseTestCase(TestCase):

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
            # TODO Use generators to yield values just when need
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

    def assertResultSet(self, result_set, *expected_tuples):
        for line, expected in enumerate(expected_tuples, start=1):
            self.assertTupleEqual(result_set.fetchone(), expected, msg='Line ' + str(line))

        self.assertIsNone(result_set.fetchone(), msg='Line ' + str(line))

    def load_file(self, filename: str, module__file__):
        module_path = os.path.dirname(module__file__)

        file_path = os.path.join(module_path, filename)

        return open(file_path)

    def clean_sequence_for_comparison(self, data):
        return data if isinstance(data, Sequence) else [ line.rstrip('\n') for line in data ]

    def assertWithFile(self, stdout, module__file__: str, filename: str, msg=None):
        with self.load_file(filename, module__file__) as expected_file:
            expected = self.clean_sequence_for_comparison(expected_file)

            actual = self.clean_sequence_for_comparison(stdout)

            self.assertSequenceEqual(actual, expected, msg)


class DBCommandsTestCase(BaseTestCase):

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


class ContaCommandTests(BaseTestCase):

    def test_conta_add_should_create_new_conta(self):
        self._call_fdc('db', 'init', for_command='conta add')

        self._call_fdc('conta', 'add', 'conta_teste')

        with self.runsql('select rowid, nome from conta;') as rs:
            self.assertResultSet(rs, (1, 'conta_teste'))

    def test_conta_list_should_list_contas(self):
        self._call_fdc('db', 'init', for_command='conta list')

        self._call_fdc('conta', 'add', 'conta_1', for_command='conta list')

        self._call_fdc('conta', 'add', 'conta_2', for_command='conta list')

        stdout = self._call_fdc('conta', 'list')

        self.assertWithFile(stdout, __file__, 'expected_conta_list')


if __name__ == '__main__':
    unittest.main()
