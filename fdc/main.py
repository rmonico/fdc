#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from argparse_helpers.parsers.date_parser import date_parser
from di_container.injector import di_container


class Main(object):

    def __init__(self):
        self._root_commands = []

    def main(self):
        di_container.load_resources(__package__)

        args = self.parse_command_line()

        command_instance = args.clazz()

        di_container.inject_resources(command_instance)

        command_instance.run(args)

    def parse_command_line(self):
        parser = argparse.ArgumentParser()

        subparsers = parser.add_subparsers()

        di_container.create_resource(name='root_parser', instance=subparsers)

        di_container.event('root_parser_created')

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


if __name__ == '__main__':
    Main().main()
