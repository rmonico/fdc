from commons.abstract_dao import AbstractDao
from commons.sqlbuilder import TableDescriptor
from commons.rowwrapper import RowWrapper
from converters import date

lancamento_table_descriptor = TableDescriptor('lancamento', 'rowid', 'data', 'origem', 'destino', 'valor', 'observacao',
                                              'produto', 'quantidade', 'fornecedor')


class Lancamento(object):

    def __init__(self):
        lancamento_table_descriptor.create_field_attributes(self)


class Conta(RowWrapper):
    pass


Conta.create_field('nome')
Conta.create_field('propriedades')


class LancamentoWithContas(RowWrapper):
    pass


LancamentoWithContas.create_field('data', lambda row, offset: date.parse(row[offset]), 1)
LancamentoWithContas.create_field('origem', Conta)
LancamentoWithContas.create_field('destino', Conta)
LancamentoWithContas.create_field('valor')
LancamentoWithContas.create_field('observacao')


class LancamentoDao(AbstractDao):

    def __init__(self):
        super().__init__(Lancamento, lancamento_table_descriptor)

    def list_with_contas(self):
        # TODO Support where
        # TODO Move the construction of this select to SelectBuilder
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
