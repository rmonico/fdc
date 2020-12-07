import os
import subprocess
from unittest import TestCase


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
        import shutil

        shutil.rmtree(self._env('FDC_FOLDER'))

        os.remove(self._env('FDCRC'))

    def _call_fdc(self, *args):
        return subprocess.run(['fdc'] + list(args), env=self._environment, stdout=subprocess.PIPE)

    def test_db_init(self):
        result = self._call_fdc('db', 'init')

        self.assertEqual(result.returncode, 0)

        database_filename = self._env('FDC_FOLDER') + '/main.db'

        self.assertTrue(os.path.exists(self._env('FDCRC')))
        self.assertTrue(os.path.exists(database_filename))

        import sqlite3

        conn = sqlite3.connect(database_filename)

        rs = conn.execute("select * from sqlite_master where type='table';")

        tables = ['Conta', 'Cotacao', 'Orcamento', 'OrcamentoLancamento', 'Lancamento', 'Produto', 'Fornecedor']

        table_count = 0

        for row in rs:
            table = row[1]

            self.assertTrue(table in tables, '"{}" is not in table list'.format(table))

            table_count += 1

        self.assertEqual(table_count, 7, msg='Wrong table count')

    def test_db_restore(self):
        file = open(self._env('FDC_FOLDER') + '/main.dump', 'w')

        file.write('create table test(column)')

        file.close()

        result = self._call_fdc('db', 'restore')

        database_filename = self._env('FDC_FOLDER') + '/main.db'


if __name__ == '__main__':
    unittest.main()




