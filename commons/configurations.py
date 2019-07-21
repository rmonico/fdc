class Configurations(object):

    def __init__(self, configs):
        self._configs = configs

    def get(self, qualified_key):
        return self._configs[qualified_key]


class ConfigurationFactory(object):

    @staticmethod
    def get_external_resources():
        return [{'name': 'app configuration', 'creator': ConfigurationFactory._load_configurations}]

    def _load_configurations(self):
        # TODO Load this from file
        import os

        db_folder = '{HOME}/.config/fdc'.format(**os.environ)
        db_path = '{}/database.db'.format(db_folder)

        log_level = 'INFO'

        return {'db': {'folder': db_folder, 'path': db_path}, 'log': {'verbosity': log_level}}
