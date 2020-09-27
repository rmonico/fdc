from commons.abstract_dao import AbstractDao
from commons.sqlbuilder import TableDescriptor

from types import SimpleNamespace


lancamento_table_descriptor = TableDescriptor('lancamento', 'rowid', 'data', 'origem', 'destino', 'valor', 'observacao',
                                              'produto', 'quantidade', 'fornecedor')


class Lancamento(object):

    def __init__(self):
        lancamento_table_descriptor.create_field_attributes(self)


class LancamentoDao(AbstractDao):

    def __init__(self):
        super().__init__(Lancamento, lancamento_table_descriptor)


    def list_with_contas(self):
        # TODO Support where
        query = 'select\
    lancamento.data as data,\
    origem.nome as origem_nome,\
    origem.propriedades as origem_propriedades,\
    destino.nome as destino_nome,\
    destino.propriedades as destino_propriedades,\
    lancamento.valor as valor\
 \
from\
    lancamento as lancamento\
\
    left join conta as origem on\
        (lancamento.origem=origem.rowid)\
\
    left join conta as destino on\
        (lancamento.destino=destino.rowid)\
\
order by\
    lancamento.data asc'

        cursor = self._connection.execute(query)

        result = list()

        for line in cursor:
            row = dict()

            row['data'] = line[0]
            row['origem'] = SimpleNamespace(nome=line[1], propriedades=line[2])
            row['destino'] = SimpleNamespace(nome=line[3], propriedades=line[4])
            row['valor'] = line[5]

            result.append(SimpleNamespace(**row))

        return result


    @staticmethod
    def injectable_resource():
        return 'lancamento dao'
