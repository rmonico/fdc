from datetime import datetime
from decimal import Decimal, InvalidOperation

from di_container.injector import Inject

_CSV_DATE_FORMAT = '%d/%b/%Y'


class ImportCSVCommand(object):

    def __init__(self):
        self._conta_dao = Inject('conta dao')
        self._produto_dao = Inject('produto dao')
        self._fornecedor_dao = Inject('fornecedor dao')

        self._unknown_contas = None
        self._unknown_produtos = None
        self._unknown_fornecedores = None
        self._ok = None

    @staticmethod
    def import_parser_created_handler(import_parser):
        import_csv_parser = import_parser.add_parser('csv', help='Importa um arquivo .csv')
        import_csv_parser.set_defaults(event='import_csv_command')

        import_csv_parser.add_argument("filename", help="Nome do arquivo que será importado")

    def import_csv_command_handler(self, args):
        source = open(args.filename, 'r')

        self._unknown_contas = set()
        self._unknown_produtos = set()
        self._unknown_fornecedores = set()

        self._ok = True

        for self._i, self._line in enumerate(source):
            fields_array = self._get_fields_array()

            if not len(fields_array) >= 4:
                self._error('every line must have at least 4 fields'.format(param))
                continue

            fields = self._get_fields(fields_array)

            self._validate_fields(fields)

        if self._ok:
            return 'ok', {'filename': args.filename}
        else:
            return 'error', {'filename': args.filename, 'unknown_contas': self._unknown_contas,
                             'unknown_produtos': self._unknown_produtos,
                             'unknown_fornecedores': self._unknown_fornecedores}

    def _validate_fields(self, fields):
        data, origem, destino, valor, observacoes, produto, quantidade, fornecedor = fields

        if not self._data_ok(data):
            self._error('date "{}" is not in format "{}"'.format(data, _CSV_DATE_FORMAT))

        if not self._conta_dao.exists(origem):
            self._error('origem "{}" doesnt exists'.format(origem))
            self._unknown_contas.add(origem)

        if not self._conta_dao.exists(destino):
            self._error('destino "{}" doesnt exists'.format(destino))
            self._unknown_contas.add(destino)

        if not self._valor_ok(valor):
            self._error('valor "{}" is not in valid format'.format(valor))

        if produto and not self._produto_dao.exists(produto):
            self._error('produto "{}" not found'.format(produto))
            self._unknown_produtos.add(produto)

        if quantidade and not self._is_float(quantidade):
            self._error('quantidade "{}" is not a float value'.format(quantidade))

        if fornecedor and not self._fornecedor_dao.exists(fornecedor):
            self._error('fornecedor "{}" not found'.format(fornecedor))
            self._unknown_fornecedores.add(fornecedor)

    def _get_fields_array(self):
        if self._line.endswith('\n'):
            self._line = self._line[:-1]

        fields = self._line.split(';')

        return fields

    def _get_fields(self, fields_array):
        data = fields_array[0]
        origem = fields_array[1]
        destino = fields_array[2]
        valor = fields_array[3]

        observacoes = self._get(fields_array, 4)
        produto = self._get(fields_array, 5)
        quantidade = self._get(fields_array, 6)
        fornecedor = self._get(fields_array, 7)

        return data, origem, destino, valor, observacoes, produto, quantidade, fornecedor

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
