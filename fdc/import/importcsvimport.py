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

        ok = True

        for self._i, self._line in enumerate(source):
            fields_array = self._get_fields_array()

            if not self._validate(fields_array, lambda f: len(f) >= 4, None, 'every line must have at least 4 fields'):
                continue

            fields = self._get_fields(fields_array)

            ok &= self._validate_fields(fields)

        if ok:
            return 'ok', {'filename': args.filename}
        else:
            return 'error', {'filename': args.filename, 'unknown_contas': self._unknown_contas,
                             'unknown_produtos': self._unknown_produtos,
                             'unknown_fornecedores': self._unknown_fornecedores}

    def _validate_fields(self, fields):
        data, origem, destino, valor, observacoes, produto, quantidade, fornecedor = fields

        ok = self._validate(data, self._data_ok, None, 'date "{{}}" is not in format "{}"'.format(_CSV_DATE_FORMAT))

        ok &= self._validate(origem, self._conta_dao.exists, lambda: self._unknown_contas.add(origem),
                             'origem "{}" doesnt exists')

        ok &= self._validate(destino, self._conta_dao.exists, lambda: self._unknown_contas.add(destino),
                             'destino "{}" doesnt exists')

        ok &= self._validate(valor, self._valor_ok, None, 'valor "{}" is not in valid format')

        if produto:
            ok &= self._validate(produto, self._produto_dao.exists, lambda: self._unknown_produtos.add(produto),
                                 'produto "{}" not found')

        if quantidade:
            ok &= self._validate(quantidade, self._is_float, None, 'quantidade "{}" is not a float value')

        if fornecedor:
            ok &= self._validate(fornecedor, self._fornecedor_dao.exists,
                                 lambda: self._unknown_fornecedores.add(fornecedor), 'fornecedor "{}" not found')

        return ok

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

    def _validate(self, data, validator, validation_fail_callback, message):
        if not validator(data):
            print('[ERROR] Line {}: {}'.format(self._i + 1, message.format(data)))

            if validation_fail_callback:
                validation_fail_callback()

            return False

        return True

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

    @staticmethod
    def _valor_ok(valor):
        try:
            # TODO Internacionalize this to work with , for decimal point!
            Decimal(valor)
            return True
        except InvalidOperation:
            return False

    @staticmethod
    def _is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def import_csv_command_ok_handler(filename):
        print('Arquivo "{}" importado com sucesso!'.format(filename))

    @staticmethod
    def import_csv_command_error_handler(filename, unknown_contas, unknown_produtos, unknown_fornecedores):
        print('Erros importando arquivo "{}"!'.format(filename))
        print()

        ImportCSVCommand._print_array('Contas desconhecidas:', unknown_contas)
        ImportCSVCommand._print_array('Produtos desconhecidos:', unknown_produtos)
        ImportCSVCommand._print_array('Fornecedores desconhecidos:', unknown_fornecedores)

    @staticmethod
    def _print_array(message, array):
        if len(array) == 0:
            return

        print(message)

        for conta in array:
            print(conta)

        print()
