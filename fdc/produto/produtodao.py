from commons.abstract_dao import AbstractDao
from commons.sqlbuilder import TableDescriptor

produto_table_descriptor = TableDescriptor('produto', 'rowid', 'nome', 'medida', 'unidade')


class Produto(object):

    def __init__(self):
        produto_table_descriptor.create_field_attributes(self)


class ProdutoDao(AbstractDao):

    def __init__(self):
        super().__init__(Produto, produto_table_descriptor)

    @staticmethod
    def injectable_resource():
        return 'produto dao'

    def by_name(self, produto_name):
        names = produto_name.split(' ')

        if len(names) >= 3:
            nome = ' '.join(names[0:-2])
            medida = names[-2]
            unidade = names[-1]

            return self.exists('nome=? or (nome=? and medida=? and unidade=?)', produto_name, nome, medida, unidade)
        else:
            return self.exists('nome = ?', produto_name)
