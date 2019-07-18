from di_container.injector import Inject


class Configurations(object):

    def __init__(self):
        self._logger = Inject('logger')

    @staticmethod
    def get_external_resources():
        return [{'name': 'app configuration', 'creator': Configurations._load_configurations}]

    def _visit_configs(self, visitor):
        self._visit_config(None, self._configs, visitor)

    def _visit_config(self, parent_key, configs, visitor):
        for key, value in configs.items():
            if parent_key:
                qualified_key = parent_key + '.' + key
            else:
                qualified_key = key

            if isinstance(value, dict):
                self._visit_config(qualified_key, value, visitor)
            else:
                visitor(qualified_key, value)

    def _load_configurations(self):
        # TODO Load this from file
        import os

        db_folder = '{HOME}/.config/fdc'.format(**os.environ)
        db_path = '{}/database.db'.format(db_folder)

        self._configs = {'db': {'folder': db_folder, 'path': db_path}}

        self._logger.info('Loaded configs:')

        self._visit_configs(lambda key, value: self._logger.info('  {}={}'.format(key, value)))

        return self._configs
