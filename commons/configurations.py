class Configurations(object):

    def __init__(self, configs):
        self._configs = configs

    def get(self, qualified_key):
        return 'value'

    def _get(self, value, remaining_key):
        if isinstance(value, dict):
            dot_index = remaining_key.index('.')


            first_key = remaining_key[0:dot_index]
            subvalue = value[first_key]
            return self._get()
        else:
            return value


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
