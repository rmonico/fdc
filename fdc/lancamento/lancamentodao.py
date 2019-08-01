from di_container.injector import Inject


class Lancamento(object):

    def __init__(self):
        self.data = None
        self.origem = None
        self.destino = None
        self.valor = None
        self.observacoes = None
        self.produto = None
        self.quantidade = None
        self.fornecedor = None


class LancamentoDao(object):
    def __init__(self):
        self._connection = Inject('database connection')

    @staticmethod
    def injectable_resource():
        return 'lancamento dao'

    def insert(self, lancamento):
        print('inserting lancamento with: {}, {}, {}, {}, {}, {}, {}, {}'.format(lancamento.data, lancamento.origem,
                                                                                 lancamento.destino,
                                                                                 lancamento.valor,
                                                                                 lancamento.observacoes,
                                                                                 lancamento.produto,
                                                                                 lancamento.quantidade,
                                                                                 lancamento.fornecedor))
