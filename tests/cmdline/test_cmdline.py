import os
import subprocess
from unittest import TestCase


class CommandLineTestCase(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

        self.assertTrue(os.path.exists(self._env('FDCRC')))
        self.assertTrue(os.path.exists(self._env('FDC_FOLDER')))


if __name__ == '__main__':
    unittest.main()
