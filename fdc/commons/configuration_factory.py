import os

import yaml

from commons.configurations import Configurations


class ConfigurationFactory(object):

    @staticmethod
    def get_external_resources():
        return [{'name': 'app configuration', 'creator': ConfigurationFactory._load_configurations}]

    def _load_configurations(self):
        defaults = self._load_defaults()

        user_configs = self._load_user_configs()

        configs = self._make_virtual_attributes({**defaults, **user_configs})

        self._replace_values_with_environment_variables(configs)

        return Configurations(configs)

    @staticmethod
    def _load_defaults():
        stream = open("defaults.yaml", 'r')

        return yaml.safe_load(stream)

    @staticmethod
    def _load_user_configs():
        user_configs_file_path = os.environ.get('FDCRC', '{HOME}/.fdcrc'.format(**os.environ))

        stream = open(user_configs_file_path, 'r')

        return yaml.safe_load(stream)

    @staticmethod
    def _make_virtual_attributes(configs):
        configs['fdc']['db_full_path'] = '{}/{}'.format(configs['fdc']['folder'], configs['fdc']['db_file_name'])
        configs['fdc']['full_path'] = '{}/{}'.format(configs['fdc']['folder'], configs['dump']['file_name'])

        return configs

    @staticmethod
    def _replace_values_with_environment_variables(config):
        # import ipdb; ipdb.set_trace()

        for key, value in config.items():
            if isinstance(value, str):
                config[key] = value.format(**os.environ)
            elif isinstance(value, dict):
                ConfigurationFactory._replace_values_with_environment_variables(config[key])
