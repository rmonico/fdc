from di_container.injector import Inject
from commons.sqlbuilder import TableDescriptor, SelectBuilder
from types import SimpleNamespace

conta_table_descriptor = TableDescriptor('conta', 'rowid', 'nome', 'descricao', 'data_aquisicao', 'propriedades',
                                         'observacao')


class Conta(object):

    def __init__(self):
        conta_table_descriptor.create_field_attributes(self)


class ContaDao(object):

    def __init__(self):
        self._connection = Inject('database connection')

    @staticmethod
    def injectable_resource():
        return 'conta dao'

    def list(self):
        builder = SelectBuilder(conta_table_descriptor)
        query = builder.build()

        cursor = self._connection.execute(query)

        conta_list = []

        for row in cursor:
            conta = builder.load_row(row)

            conta_list.append(conta)

        cursor.close()

        return conta_list

    def by_name(self, conta_name):
        builder = SelectBuilder(conta_table_descriptor)
        builder.where('nome = ?')

        query = builder.build()

        cursor = self._connection.execute(query, (conta_name, ))

        row = cursor.fetchone()

        cursor.close()

        if row:
            return builder.load_row(row)
        else:
            return None

    def exists(self, conta_name):
        builder = SelectBuilder(conta_table_descriptor)
        builder.fields('count(*)')
        builder.where('nome = ?')

        query = builder.build()

        cursor = self._connection.execute(query, (conta_name,))

        data = cursor.fetchone()

        return data[0] == 1

    def insert(self, conta):
        # TODO Extract these code to a InsertBuilder class (maybe on connection
        # module, not sure yet)
        fields = conta.nome, conta.contabilizavel
        field_names = ["nome", "contabilizavel"]
        value_mask = "?, ?"

        if hasattr(conta, "fechamento"):
            fields += conta.fechamento,
            field_names += ["fechamento"]
            value_mask += ", ?"

        sql = "insert into conta ({fields}) values ({value_mask});".format(
            fields=", ".join(field_names), value_mask=value_mask)

        cursor = self._connection.execute(sql, fields)

        self._connection.commit()

        cursor.close()
