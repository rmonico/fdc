from datetime import datetime
from decimal import Decimal, InvalidOperation

from di_container.injector import Inject

_CSV_DATE_FORMAT = '%d/%b/%Y'


class ImportCSVCommand(object):

    def __init__(self):
        self._conta_dao = Inject('conta dao')
        self._produto_dao = Inject('produto dao')
        self._fornecedor_dao = Inject('fornecedor dao')

        self._ok = True

    @staticmethod
    def import_parser_created_handler(import_parser):
        import_csv_parser = import_parser.add_parser('csv', help='Importa um arquivo .csv')
        import_csv_parser.set_defaults(event='import_csv_command')

        import_csv_parser.add_argument("filename", help="Nome do arquivo que será importado")

    def import_csv_command_handler(self, args):
        source = open(args.filename, 'r')

        self._ok = True

        unknown_contas = set()
        unknown_produtos = set()
        unknown_fornecedores = set()

        for self._i, self._line in enumerate(source):
            line = self._line

            if line.endswith('\n'):
                line = line[:-1]

            fields = line.split(';')

            if not len(fields) >= 4:
                self._error('every line must have at least 4 fields'.format(param))
                continue

            data = fields[0]
            origem = fields[1]
            destino = fields[2]
            valor = fields[3]

            observacoes = self._get(fields, 4)
            produto = self._get(fields, 5)
            quantidade = self._get(fields, 6)
            fornecedor = self._get(fields, 7)

            if not self._data_ok(data):
                self._error('date "{}" is not in format "{}"'.format(data, _CSV_DATE_FORMAT))

            if not self._conta_dao.exists(origem):
                self._error('origem "{}" doesnt exists'.format(origem))
                unknown_contas.add(origem)

            if not self._conta_dao.exists(destino):
                self._error('destino "{}" doesnt exists'.format(destino))
                unknown_contas.add(destino)

            if not self._valor_ok(valor):
                self._error('valor "{}" is not in valid format'.format(valor))

            if produto and not self._produto_dao.exists(produto):
                self._error('produto "{}" not found'.format(produto))
                unknown_produtos.add(produto)

            if quantidade and not self._is_float(quantidade):
                self._error('quantidade "{}" is not a float value'.format(quantidade))

            if fornecedor and not self._fornecedor_dao.exists(fornecedor):
                self._error('fornecedor "{}" not found'.format(fornecedor))
                unknown_fornecedores.add(fornecedor)

        if self._ok:
            return 'ok', {'filename': args.filename}
        else:
            return 'error', {'filename': args.filename, 'unknown_contas': unknown_contas,
                             'unknown_produtos': unknown_produtos, 'unknown_fornecedores': unknown_fornecedores}

    def _error(self, message):
        print('[ERROR] Line {}: {}'.format(self._i + 1, message))

        self._ok = False

    @staticmethod
    def _get(fields, index, default=None):
        return fields[index] if len(fields) >= index + 1 else default

    @staticmethod
    def _data_ok(value):
        try:
            datetime.strptime(value, _CSV_DATE_FORMAT)

            return True
        except ValueError:
            return False

    def _valor_ok(self, valor):
        try:
            # TODO Internacionalize this to work with , for decimal point!
            Decimal(valor)
            return True
        except InvalidOperation:
            return False

    def _is_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def import_csv_command_ok_handler(self, filename):
        print('Arquivo "{}" importado com sucesso!'.format(filename))

    def import_csv_command_error_handler(self, filename, unknown_contas, unknown_produtos, unknown_fornecedores):
        print('Erros importando arquivo "{}"!'.format(filename))
        print()

        self._print_array('Contas desconhecidas:', unknown_contas)
        self._print_array('Produtos desconhecidos:', unknown_produtos)
        self._print_array('Fornecedores desconhecidos:', unknown_fornecedores)

    def _print_array(self, message, array):
        if len(array) == 0:
            return

        print(message)

        for conta in array:
            print(conta)

        print()
