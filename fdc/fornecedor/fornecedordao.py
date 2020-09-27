from di_container.injector import Inject


class FornecedorDao(object):

    def __init__(self):
        self._connection = Inject('database connection')

    @staticmethod
    def injectable_resource():
        return 'fornecedor dao'
