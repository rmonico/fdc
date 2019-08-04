from commons.configurations import Configurations


class TestConfiguration(Configurations):

    def __init__(self):
        super().__init__(self._get_configs())

    @staticmethod
    def _get_configs():
        return {'fdc': {'db_full_path': ':memory:'}, 'log': {'verbosity': 'NONE'}}

    @staticmethod
    def injectable_resource():
        return 'app configuration'
