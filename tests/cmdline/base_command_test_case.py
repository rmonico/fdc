import os
import subprocess
from unittest import TestCase
import sqlite3
import shutil
from contextlib import contextmanager
from collections.abc import Sequence


class BaseCommandTestCase(TestCase):

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

    def get_db_file(self):
        return self._env('FDC_FOLDER') + '/main.db'

    @contextmanager
    def runsql(self, sql: str):
        with sqlite3.connect(self.get_db_file()) as connection:
            result_set = connection.execute(sql)

            try:
                yield result_set
            finally:
                result_set.close()

    def runscript(self, script: str):
        with sqlite3.connect(self.get_db_file()) as connection:
            connection.executescript(script)

    def assertResultSet(self, result_set, *expected_tuples):
        for line, expected in enumerate(expected_tuples, start=1):
            self.assertTupleEqual(result_set.fetchone(), expected, msg='Line ' + str(line))

        self.assertIsNone(result_set.fetchone(), msg='Line ' + str(line))

    def load_file(self, filename: str, module__file__):
        module_path = os.path.dirname(module__file__)

        file_path = os.path.join(module_path, filename)

        return open(file_path)

    def clean_sequence_for_comparison(self, data):
        return data if isinstance(data, Sequence) else [line.rstrip('\n') for line in data]

    def assertWithFile(self, stdout, module__file__: str, filename: str, msg=None):
        with self.load_file(filename, module__file__) as expected_file:
            expected = self.clean_sequence_for_comparison(expected_file)

            actual = self.clean_sequence_for_comparison(stdout)

            self.assertSequenceEqual(actual, expected, msg)


if __name__ == '__main__':
    unittest.main()
