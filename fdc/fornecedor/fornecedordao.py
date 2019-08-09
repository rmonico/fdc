from commons.abstract_dao import AbstractDao
from commons.sqlbuilder import TableDescriptor

fornecedor_table_descriptor = TableDescriptor('fornecedor', 'rowid', 'nome')


class Fornecedor(object):

    def __init__(self):
        fornecedor_table_descriptor.create_field_attributes(self)


class FornecedorDao(AbstractDao):

    def __init__(self):
        super().__init__(Fornecedor, fornecedor_table_descriptor)

    @staticmethod
    def injectable_resource():
        return 'fornecedor dao'

    def by_name(self, fornecedor_name):
        return self.get_single('nome=?', fornecedor_name)
