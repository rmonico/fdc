#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

from argparse_helpers.parsers.date_parser import date_parser
from di_container.controller import controller
from di_container.injector import di_container


class Main(object):

    def __init__(self):
        self._root_commands = []

    def main(self):
        packages = [__package__, __package__ + '.conta', __package__ + '.database', __package__ + '.command', 'commons', ]

        di_container.load_resources(packages)
        controller.load_listeners(packages)

        di_container.inject_resources(self)

        args = self.parse_command_line()

        command_results = controller.event(args.event, args=args)

        command_status = command_results[0]
        command_args = command_results[1:]

        controller.event(args.event + '_' + command_status, *command_args)

    def parse_command_line(self):
        parser = argparse.ArgumentParser()

        subparsers = parser.add_subparsers()

        controller.event('root_parser_created', root_parser=subparsers)

        _make_contrato_parser(subparsers)

        return parser.parse_args()


def _make_contrato_list_parser(parent_parser):
    contrato_list_parser = parent_parser.add_parser(
        "list", help="Lista os contratos existentes")


def _make_contrato_add_parser(parent_parser):
    contrato_add_parser = parent_parser.add_parser(
        "add", help="Adiciona um novo contrato")

    contrato_add_parser.add_argument(
        "data-compra", type=date_parser, help="Data da compra. Formato: AAAA-MM-DD")
    contrato_add_parser.add_argument("conta", help="Conta associada")
    contrato_add_parser.add_argument(
        "total-parcelas", type=int, help="Total de parcelas")
    contrato_add_parser.add_argument(
        "-v", "--valor-parcela", type=float, help="Valor da parcela")
    contrato_add_parser.add_argument("-o", "--observacao", help="Observações")


def _make_contrato_parser(parent_parser):
    contrato_parser = parent_parser.add_parser(
        "contrato", help="Comandos de contrato")
    subparsers = contrato_parser.add_subparsers()

    _make_contrato_list_parser(subparsers)

    _make_contrato_add_parser(subparsers)


def entry_point():
    Main().main()


if __name__ == '__main__':
    entry_point()
