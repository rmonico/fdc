from di_container.injector import Inject

from commons.sqlbuilder import TableDescriptor, InsertBuilder

lancamento_table_descriptor = TableDescriptor('lancamento', 'data', 'origem', 'destino', 'valor', 'observacao',
                                              'produto', 'quantidade', 'fornecedor')


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
        builder = InsertBuilder()
        sql = builder.build(lancamento_table_descriptor)

        self._connection.execute(sql, lancamento_table_descriptor.get_fields_tuple(lancamento))
