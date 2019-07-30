from di_container.injector import Inject


class ProdutoDao(object):

    def __init__(self):
        self._connection = Inject('database connection')

    @staticmethod
    def injectable_resource():
        return 'produto dao'

    def exists(self, produto_name):
        # TODO
        return True
