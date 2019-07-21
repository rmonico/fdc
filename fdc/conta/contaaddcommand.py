from di_container.injector import Inject
from fdc.conta.contadao import Conta


class ContaAddCommand(object):

    def __init__(self):
        self._dao = Inject('conta dao')

    @staticmethod
    def conta_parser_created_handler(conta_parser):
        conta_add_parser = conta_parser.add_parser('add', aliases=['a'], help='Adiciona uma nova conta')
        conta_add_parser.set_defaults(event='conta_add_command')

        conta_add_parser.add_argument("-c", "--contabilizavel", default=False, action="store_true",
                                      help="Marca a nova conta como contabilizável (o saldo é calculado nas listagens)")
        conta_add_parser.add_argument("--df", "--fechamento", help="Data de fechamento da conta")

        conta_add_parser.add_argument("nome", help="Nome da conta a ser criada")

    def conta_add_command_handler(self, args):
        conta = Conta()

        conta.nome = args.nome
        conta.contabilizavel = args.contabilizavel

        if hasattr(args, "fechamento"):
            conta.fechamento = args.fechamento

        self._dao.insert(conta)

        return 'ok', conta

    def conta_add_command_ok_handler(self, conta):
        message = 'Conta \'{}\' ({}contabilizável) criada'.format(conta.nome,
                                                                  'não ' if not conta.contabilizavel else '')

        print(message)
