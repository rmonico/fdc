from di_container.injector import Inject

from commons.sqlbuilder import TableDescriptor, InsertBuilder

lancamento_table_descriptor = TableDescriptor('lancamento', 'rowid', 'data', 'origem', 'destino', 'valor', 'observacao',
                                              'produto', 'quantidade', 'fornecedor')


class Lancamento(object):

    def __init__(self):
        lancamento_table_descriptor.create_field_attributes(self)


class LancamentoDao(object):
    def __init__(self):
        self._connection = Inject('database connection')

    @staticmethod
    def injectable_resource():
        return 'lancamento dao'

    def insert(self, lancamento):
        builder = InsertBuilder(lancamento_table_descriptor)
        sql = builder.build()

        self._connection.execute(sql, builder.get_field_values(lancamento))
