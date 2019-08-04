from di_container.injector import Inject


class ProdutoDao(object):

    def __init__(self):
        self._connection = Inject('database connection')

    @staticmethod
    def injectable_resource():
        return 'produto dao'

    def exists(self, produto_name):
        names = produto_name.split(' ')

        if len(names) >= 3:
            nome = ' '.join(names[0:-2])
            medida = names[-2]
            unidade = names[-1]

            cursor = self._connection.execute(
                'select count(*) from produto where nome=? or (nome=? and medida=? and unidade=?);',
                (produto_name, nome, medida, unidade))
        else:
            cursor = self._connection.execute('select count(*) from produto where nome=?;', (produto_name,))

        data = cursor.fetchone()

        return data[0] == 1
