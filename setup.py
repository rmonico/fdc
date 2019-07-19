from setuptools import setup

setup(name='fdc',
      version='0.1',
      description='Fluxo De Caixa, a cli client to personal cash flow',
      url='https://github.com/rmonico/fdc',
      author='Rafael Monico',
      author_email='rmonico1@gmail.com',
      license='GPL3',
      packages=['fdc', 'fdc.conta', 'fdc.command', 'fdc.database', 'argparse_helpers.parsers', 'commons', 'di_container', ],
      entry_points={
          'console_scripts': ['fdc=fdc.main:entry_point'],
      },
      zip_safe=False, install_requires=['ipdb'])
