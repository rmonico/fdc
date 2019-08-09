from datetime import datetime
from decimal import Decimal, InvalidOperation

from di_container.injector import Inject
from fdc.lancamento.lancamentodao import Lancamento

_CSV_DATE_FORMAT = '%d/%b/%Y'


class ImportCSVCommand(object):

    def __init__(self):
        self._connection = Inject('database connection')
        self._conta_dao = Inject('conta dao')
        self._produto_dao = Inject('produto dao')
        self._fornecedor_dao = Inject('fornecedor dao')
        self._lancamento_dao = Inject('lancamento dao')

        self._unknown_contas = None
        self._unknown_produtos = None
        self._unknown_fornecedores = None

    @staticmethod
    def import_parser_created_handler(import_parser):
        import_csv_parser = import_parser.add_parser('csv', help='Importa um arquivo .csv')
        import_csv_parser.set_defaults(event='import_csv_command')

        import_csv_parser.add_argument('-c', '--confirm', action='store_true',
                                       help='Confirma a importação, caso contrário apenas mostra em tela o que será importado')
        import_csv_parser.add_argument("filename", help="Nome do arquivo que será importado")

    def import_csv_command_handler(self, args):
        source = open(args.filename, 'r')

        self._unknown_contas = set()
        self._unknown_produtos = set()
        self._unknown_fornecedores = set()

        ok = True

        lancamentos = []

        try:
            for self._i, self._line in enumerate(source):
                fields_array = self._get_fields_array()

                if not self._validate(fields_array, lambda f: len(f) >= 4, None,
                                      'every line must have at least 4 fields'):
                    continue

                fields = self._get_fields(fields_array)

                ok &= self._validate_fields(*fields)

                if ok:
                    lancamento = self._make_lancamento(*fields)

                    if args.confirm:
                        self._lancamento_dao.insert(lancamento)
                    else:
                        lancamentos.append(lancamento)

        except Exception:
            self._connection.rollback()
            raise

        if ok:
            if args.confirm:
                self._connection.commit()

                return 'imported', {'filename': args.filename}
            else:
                return 'simulated', {'filename': args.filename, 'lancamentos': lancamentos}

        else:
            if args.confirm:
                self._connection.rollback()

            return 'error', {'filename': args.filename, 'unknown_contas': self._unknown_contas,
                             'unknown_produtos': self._unknown_produtos,
                             'unknown_fornecedores': self._unknown_fornecedores}

    def _get_fields_array(self):
        if self._line.endswith('\n'):
            self._line = self._line[:-1]

        fields = self._line.split(';')

        return fields

    def _validate(self, data, validator, validation_fail_callback, message):
        if not validator(data):
            print('[ERROR] Line {}: {}'.format(self._i + 1, message.format(data)))

            if validation_fail_callback:
                validation_fail_callback()

            return False

        return True

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

    def _validate_fields(self, data, origem, destino, valor, observacoes, produto, quantidade, fornecedor):
        ok = self._validate(data, self._data_ok, None, 'date "{{}}" is not in format "{}"'.format(_CSV_DATE_FORMAT))

        ok &= self._validate(origem, self._conta_dao.by_name, lambda: self._unknown_contas.add(origem),
                             'origem "{}" doesnt exists')

        ok &= self._validate(destino, self._conta_dao.by_name, lambda: self._unknown_contas.add(destino),
                             'destino "{}" doesnt exists')

        ok &= self._validate(valor, self._valor_ok, None, 'valor "{}" is not in valid format')

        if produto:
            ok &= self._validate(produto, self._produto_dao.by_name, lambda: self._unknown_produtos.add(produto),
                                 'produto "{}" not found')

        if quantidade:
            ok &= self._validate(quantidade, self._is_float, None, 'quantidade "{}" is not a float value')

        if fornecedor:
            ok &= self._validate(fornecedor, self._fornecedor_dao.by_name,
                                 lambda: self._unknown_fornecedores.add(fornecedor), 'fornecedor "{}" not found')

        return ok

    def _make_lancamento(self, data, origem, destino, valor, observacoes, produto, quantidade, fornecedor):
        lancamento = Lancamento()

        lancamento.data = data
        lancamento.valor = int(valor.replace('.', ''))
        lancamento.origem = self._conta_dao.by_name(origem)
        lancamento.destino = self._conta_dao.by_name(destino)
        lancamento.observacoes = observacoes
        lancamento.produto = self._produto_dao.by_name(produto) if produto else None
        lancamento.quantidade = quantidade
        lancamento.fornecedor = self._fornecedor_dao.by_name(fornecedor) if fornecedor else None

        return lancamento

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
    def import_csv_command_imported_handler(filename):
        print('Arquivo "{}" importado com sucesso!'.format(filename))

    @staticmethod
    def import_csv_command_simulated_handler(filename, lancamentos):
        print('Simulated import for file "{}" (use --confirm to actually import), would create lancamentos:'.format(
            filename))

        for lancamento in lancamentos:
            print(ImportCSVCommand._make_lancamento_string(lancamento))

    @staticmethod
    def _make_lancamento_string(lancamento):
        values = list()

        values.append(str(lancamento.data))
        values.append(str(lancamento.origem))
        values.append(str(lancamento.destino))
        values.append(str(lancamento.valor))
        values.append(str(lancamento.observacoes)) if lancamento.observacoes else None
        values.append(str(lancamento.produto)) if lancamento.produto else None
        values.append(str(lancamento.quantidade)) if lancamento.quantidade else None
        values.append(str(lancamento.fornecedor)) if lancamento.fornecedor else None

        return '; '.join(values)

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
