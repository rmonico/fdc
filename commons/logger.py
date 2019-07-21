
_NONE = 0
_INFO = 1


class Logger(object):

    def __init__(self):
        self._verbosity_level = _NONE

    @staticmethod
    def injectable_resource():
        return 'logger'

    def info(self, message, *args, **kwargs):
        if self._verbosity_level >= _INFO:
            print(message.format(*args, **kwargs))
