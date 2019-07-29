from commons.git_wrapper import GitWrapper


class FDCGitWrapperFactory(object):

    def __init__(self):
        self._configs = Inject('app configuration')
        self._logger = Inject('logger')

    @staticmethod
    def get_external_resources():
        return [{'name': 'fdc git wrapper', 'creator': FDCGitWrapperFactory.create_wrapper}]

    def create_wrapper(self):
        return GitWrapper(self._configs['fdc.folder'])
