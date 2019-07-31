from di_container.injector import Inject


class FornecedorDao(object):

    def __init__(self):
        self._connection = Inject('database connection')

    @staticmethod
    def injectable_resource():
        return 'fornecedor dao'

    def exists(self, fornecedor_name):
        cursor = self._connection.execute("select count(*) from fornecedor where nome=?;", (fornecedor_name,))

        data = cursor.fetchone()

        return data[0] == 1
