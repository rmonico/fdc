from commons.abstract_dao import AbstractDao
from commons.sqlbuilder import TableDescriptor

lancamento_table_descriptor = TableDescriptor('lancamento', 'rowid', 'data', 'origem', 'destino', 'valor', 'observacao',
                                              'produto', 'quantidade', 'fornecedor')


class Lancamento(object):

    def __init__(self):
        lancamento_table_descriptor.create_field_attributes(self)


class LancamentoDao(AbstractDao):
    def __init__(self):
        super().__init__(Lancamento, lancamento_table_descriptor)

    @staticmethod
    def injectable_resource():
        return 'lancamento dao'
