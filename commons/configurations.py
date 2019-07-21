class KeyNotFoundException(Exception):

    def __init__(self, key=None):
        if key:
            super(super.__class__).__init__('Configuration key not found: "{}"'.format(key))
        else:
            super(super.__class__).__init__()


class Configurations(object):

    def __init__(self, configs):
        self._configs = configs

    def __getitem__(self, key):
        try:
            value = self._get(self._configs, key.split('.'))
        except KeyNotFoundException:
            raise KeyNotFoundException(key)

        return value

    def _get(self, current_dict, remaining_keys):
        value = current_dict[remaining_keys[0]]

        if len(remaining_keys) == 1:
            return value

        if not isinstance(value, dict):
            raise KeyNotFoundException()

        return self._get(value, remaining_keys[1:])

    def dump(self):
        result = ''
        for key, value in self._configs.items():
            result += '{}: {}\n'.format(key, value)

        return result


class ConfigurationFactory(object):

    @staticmethod
    def get_external_resources():
        return [{'name': 'app configuration', 'creator': ConfigurationFactory._load_configurations}]

    def _load_configurations(self):
        # TODO Load this from file
        import os

        db_folder = '{HOME}/.config/fdc'.format(**os.environ)
        db_path = '{}/database.db'.format(db_folder)

        log_level = 'DEBUG'

        return Configurations({'db': {'folder': db_folder, 'path': db_path}, 'log': {'verbosity': log_level}})
