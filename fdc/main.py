import argparse

from argparse_helpers.parsers.date_parser import date_parser
from di_container.controller import controller
from di_container.injector import di_container, Inject


class Main(object):

    def __init__(self):
        self._logger = Inject('logger')
        self._configs = Inject('app configuration')

    def main(self):
        packages = ['commons', 'di_container', __package__ + '.commons', __package__ + '.conta',
                    __package__ + '.database', __package__ + '.import', 'fdc.lancamento', 'fdc.produto',
                    'fdc.fornecedor', ]

        di_container.load_resources(packages)
        controller.load_listeners(packages)

        di_container.inject_resources(self)

        self._logger.info('Loaded resources and listeners from packages: {}', packages)

        self._logger.debug('Using configurations: {}', self._configs.dump())

        args = self.parse_command_line()

        self._logger.info('Command line parsed: {}', args)

        event_results = controller.event(args.event, inject_dependencies=True, args=args)

        for result in event_results:
            self._logger.info('Calling front end for "{}" with data "{}, {}" due to status "{}"', args.event,
                              result.kwdata, result.data, result.status)

            controller.event(args.event + '_' + result.status, inject_dependencies=True, *result.data, **result.kwdata)

    def parse_command_line(self):
        parser = argparse.ArgumentParser()

        subparsers = parser.add_subparsers()

        controller.event('root_parser_created', root_parser=subparsers)

        return parser.parse_args()


def entry_point():
    Main().main()


if __name__ == '__main__':
    entry_point()
