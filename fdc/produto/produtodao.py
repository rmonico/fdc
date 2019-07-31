from di_container.injector import Inject


class ProdutoDao(object):

    def __init__(self):
        self._connection = Inject('database connection')

    @staticmethod
    def injectable_resource():
        return 'produto dao'

    def exists(self, produto_name):
        cursor = self._connection.execute("select count(*) from produto where nome=?;", (produto_name,))

        data = cursor.fetchone()

        return data[0] == 1
