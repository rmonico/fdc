from datetime import datetime
from decimal import Decimal, InvalidOperation

from di_container.injector import Inject

_CSV_DATE_FORMAT = '%d/%b/%Y'


class ImportCSVCommand(object):

    def __init__(self):
        self._status = None
        self._conta_dao = Inject('conta dao')
        self._produto_dao = Inject('produto dao')
        self._fornecedor_dao = Inject('fornecedor dao')

    @staticmethod
    def import_parser_created_handler(import_parser):
        import_csv_parser = import_parser.add_parser('csv', help='Importa um arquivo .csv')
        import_csv_parser.set_defaults(event='import_csv_command')

        import_csv_parser.add_argument("filename", help="Nome do arquivo que será importado")

    def import_csv_command_handler(self, args):
        source = open(args.filename, 'r')

        self._status = 'ok'

        for self._i, self._line in enumerate(source):
            line = self._line

            if line.endswith('\n'):
                line = line[:-1]

            fields = line.split(';')

            if not self._assert(len(fields) >= 4, 'every line must have at least 4 fields'):
                continue

            data = fields[0]
            origem = fields[1]
            destino = fields[2]
            valor = fields[3]

            observacoes = self._get(fields, 4)
            produto = self._get(fields, 5)
            quantidade = self._get(fields, 6)
            fornecedor = self._get(fields, 7)

            self._assert(self._data_ok(data), 'date "{}" is not in format "{}"', data, _CSV_DATE_FORMAT)

            self._assert(self._conta_dao.exists(origem), 'origem "{}" doesnt exists', origem)

            self._assert(self._conta_dao.exists(destino), 'destino "{}" doesnt exists', destino)

            self._assert(self._valor_ok(valor), 'valor "{}" is not in valid format', valor)

            if produto:
                self._assert(self._produto_dao.exists(produto), 'produto "{}" not found', produto)

            if quantidade:
                self._assert(self._is_float(quantidade), 'quantidade "{}" is not a float value', quantidade)

            if fornecedor:
                self._assert(self._fornecedor_dao.exists(fornecedor), 'fornecedor "{}" not found', fornecedor)

        return self._status, {'filename': args.filename}

    def _assert(self, assertion, message, *message_args, **message_kwargs):
        if not assertion:
            print('[ERROR] Line {}: {}'.format(self._i + 1, message.format(*message_args, **message_kwargs)))
            self._status = 'error'

        return assertion

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

    def import_csv_command_error_handler(self, filename):
        print('Errors importing file "{}"!'.format(filename))
