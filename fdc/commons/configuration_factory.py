from commons.configurations import Configurations


class ConfigurationFactory(object):

    @staticmethod
    def get_external_resources():
        return [{'name': 'app configuration', 'creator': ConfigurationFactory._load_configurations}]

    def _load_configurations(self):
        # TODO Load this from file
        # fdc.db_full_path is a "virtual attribute", should be created here!
        import os

        fdc_folder = '{HOME}/.config/fdc'.format(**os.environ)
        db_file_name = 'database.db'
        dump_file_name = 'dump.db'

        log_level = 'DEBUG'

        return Configurations(
            {
                'fdc': {
                    'folder': fdc_folder,
                    'db_file_name': db_file_name,
                    'db_full_path': fdc_folder + '/' + db_file_name
                },
                'dump': {
                    'file_name': dump_file_name,
                    'full_path': fdc_folder + '/' + dump_file_name
                },
                'log': {'verbosity': log_level}
            })
