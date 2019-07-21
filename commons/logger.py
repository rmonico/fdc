from di_container.injector import Inject


class Logger(object):
    _verbosity_level = {'NONE': 0, 'WARN': 1, 'INFO': 2, 'DEBUG': 3}

    def __init__(self):
        self._configs = Inject('app configuration')
        self._verbosity_level = None

    @staticmethod
    def injectable_resource():
        return 'logger'

    def message(self, message, *args, **kwargs):
        self._log(message, Logger._verbosity_level['NONE'], *args, **kwargs)

    def warn(self, message, *args, **kwargs):
        self._log(message, Logger._verbosity_level['WARN'], *args, **kwargs)

    def info(self, message, *args, **kwargs):
        self._log(message, Logger._verbosity_level['INFO'], *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        self._log(message, Logger._verbosity_level['DEBUG'], *args, **kwargs)

    def _log(self, message, level, *args, **kwargs):
        if not self._verbosity_level:
            self._verbosity_level = Logger._verbosity_level[self._configs['log.verbosity']]

        if self._verbosity_level >= level:
            print(message.format(*args, **kwargs))
