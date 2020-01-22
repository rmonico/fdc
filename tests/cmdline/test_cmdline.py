import os
import sqlite3
import subprocess
from unittest import TestCase


class CommandLineTestCase(TestCase):

    def db_at(self, database_filename):
        self._expected_tables = []

        self.assertTrue(os.path.exists(database_filename))

        self._conn = sqlite3.connect(database_filename)
        self._rs = self._conn.execute("select * from sqlite_master where type='table';")

        return self

    def has_table(self, table_name):
        self._actual_tables = []
        if self._expected_tables:
            self._expected_tables += [table_name]

            while row in self._rs:
                self._actual_tables += [row[1]]

        self.assertTrue(table_name in self._actual_tables, '"{}" is not in table list'.format(table_name))

        return self

    @staticmethod
    def field(field_name):
        # TODO Implementation
        return self

    @staticmethod
    def type(type_name):
        # TODO Implementation
        return self

    @staticmethod
    def not_null(value):
        # TODO Implementation
        return self

    def end_table(self):
        return self

    @staticmethod
    def and_no_one_else_table():
        return self

    def setUp(self):
        self._environment = os.environ.copy()

        self._env('FDCRC', '{HOME}/.unittests_fdcrc'.format(**self._environment))
        self._env('FDC_FOLDER', '{HOME}/.config/fdc_tests'.format(**self._environment))

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
        import shutil

        shutil.rmtree(self._env('FDC_FOLDER'))

        os.remove(self._env('FDCRC'))

    def _call_fdc(self, *args):
        return subprocess.run(['fdc'] + list(args), env=self._environment, stdout=subprocess.PIPE)

    def assert_has_only_this_tables(self, database_filename, tables):
        self.assertTrue(os.path.exists(self._env('FDCRC')))
        self.assertTrue(os.path.exists(database_filename))
        conn = sqlite3.connect(database_filename)
        rs = conn.execute("select * from sqlite_master where type='table';")
        table_count = 0
        for row in rs:
            table = row[1]

            self.assertTrue(table in tables, '"{}" is not in table list'.format(table))

            table_count += 1

        self.assertEqual(table_count, len(tables), msg='Wrong table count')

    def test_db_init(self):
        result = self._call_fdc('db', 'init')

        self.assertEqual(result.returncode, 0)

        database_filename = self._env('FDC_FOLDER') + '/main.db'

        self.db_at(database_filename).has_table('conta').field('nome').type('text').not_null(
            True).end_table().and_no_one_else_table()

        self.assert_has_only_this_tables(database_filename,
                                         ['Conta', 'Cotacao', 'Orcamento', 'OrcamentoLancamento', 'Lancamento',
                                          'Produto', 'Fornecedor'])

    def test_db_restore(self):
        file = open(self._env('FDC_FOLDER') + '/main.dump', 'w')

        file.write('create table test(column)')

        file.close()

        self._call_fdc('db', 'restore')

        database_filename = self._env('FDC_FOLDER') + '/main.db'

        self.db_at(database_filename).has_table('test').end_table() \
            .and_no_one_else_table()


if __name__ == '__main__':
    unittest.main()

# check fdc db init
# check fdc db restore
# check fdc db dump

# check fdc conta add
# check fdc conta list

# check fdc import csv

# check fdc lanc add
