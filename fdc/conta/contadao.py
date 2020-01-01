from commons.abstract_dao import AbstractDao
from commons.sqlbuilder import TableDescriptor

conta_table_descriptor = TableDescriptor('conta', 'rowid', 'nome', 'descricao', 'data_aquisicao', 'propriedades',
                                         'observacao')


class Conta(object):

    def __init__(self):
        conta_table_descriptor.create_field_attributes(self, nome="", propriedades="")


class ContaDao(AbstractDao):

    def __init__(self):
        super().__init__(Conta, conta_table_descriptor)

    @staticmethod
    def injectable_resource():
        return 'conta dao'

    def by_name(self, conta_name):
        return self.get_single('nome=?', conta_name)
