from commons.abstract_dao import AbstractDao
from commons.sqlbuilder import TableDescriptor
from commons.rowwrapper import RowWrapper


lancamento_table_descriptor = TableDescriptor('lancamento', 'rowid', 'data', 'origem', 'destino', 'valor', 'observacao',
                                              'produto', 'quantidade', 'fornecedor')


class Lancamento(object):

    def __init__(self):
        lancamento_table_descriptor.create_field_attributes(self)


class Conta(RowWrapper):
    pass

Conta._create_field('nome')
Conta._create_field('propriedades')

class LancamentoWithContas(RowWrapper):
    pass

LancamentoWithContas._create_field('data')
LancamentoWithContas._create_field('origem', Conta)
LancamentoWithContas._create_field('destino', Conta)
LancamentoWithContas._create_field('valor')
LancamentoWithContas._create_field('observacao')


class LancamentoDao(AbstractDao):

    def __init__(self):
        super().__init__(Lancamento, lancamento_table_descriptor)


    def list_with_contas(self):
        # TODO Support where
        # TODO Move the construction of this select to RowWrapper
        query = 'select\
    lancamento.rowid as id,\
    lancamento.data as data,\
    origem.rowid as origem_id,\
    origem.nome as origem_nome,\
    origem.propriedades as origem_propriedades,\
    destino.rowid as destino_id,\
    destino.nome as destino_nome,\
    destino.propriedades as destino_propriedades,\
    lancamento.valor as valor,\
    lancamento.observacao as observacao\
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

        return RowWrapper.load(cursor, LancamentoWithContas)


    @staticmethod
    def injectable_resource():
        return 'lancamento dao'
