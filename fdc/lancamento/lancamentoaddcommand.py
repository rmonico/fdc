from datetime import date

from argparse_helpers.parsers.currency_parser import currency_parser
from argparse_helpers.parsers.date_parser import date_parser
from di_container.injector import Inject
from .lancamentodao import Lancamento


class LancamentoAddCommand(object):

    def __init__(self):
        self._conta_dao = Inject('conta dao')
        self._lancamento_dao = Inject('lancamento dao')

    def lancamento_parser_created_handler(self, lancamento_parser):
        parser = lancamento_parser.add_parser('add', aliases=['a'], help='Adiciona um novo lançamento')
        parser.set_defaults(event='lancamento_add_command')

        parser.add_argument('origem')
        parser.add_argument('destino')
        parser.add_argument('valor', type=currency_parser)
        parser.add_argument('--data', '-d', type=date_parser, default=date.today())
        parser.add_argument('--observacao', '-o', required=False)

    def lancamento_add_command_handler(self, args):
        contas_not_found = []

        origem = self._conta_dao.by_name(args.origem)
        if not origem:
            contas_not_found += ['origem']

        destino = self._conta_dao.by_name(args.destino)
        if not destino:
            contas_not_found += ['destino']

        if len(contas_not_found) > 0:
            return 'conta_not_found', {'contas': contas_not_found}
        else:
            lancamento = Lancamento()

            lancamento.data = args.data
            lancamento.origem = origem
            lancamento.destino = destino
            lancamento.valor = Decimal(args.valor)
            lancamento.observacao = args.observacao

            self._lancamento_dao.insert(lancamento)

            return 'ok', {'lancamento': lancamento}

    def lancamento_add_command_ok_handler(self, lancamento):
        observacao = lancamento.observacao if lancamento.observacao else ''

        print(
            'Lançamento criado: {} {} {} {} {}'.format(lancamento.data, lancamento.origem.nome, lancamento.destino.nome,
                                                       lancamento.valor, observacao))

    def lancamento_add_command_conta_not_found_handler(self, contas):
        plural_suffix = 's' if len(contas) > 0 else ''

        contas_str = ', '.join(contas)

        print('Conta{} não encontrada{0}: {}'.format(plural_suffix, contas_str))
