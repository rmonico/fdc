#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from .parsers.date_parser import date_parser


def _make_conta_list_parser(parent_parser):
    conta_list_parser = parent_parser.add_parser(
        "list", help="Lista as contas existentes")


def _make_conta_add_parser(parent_parser):
    conta_add_parser = parent_parser.add_parser(
        "add", help="Adiciona uma nova conta")

    conta_add_parser.add_argument("-c", "--contabilizavel", action="store_true",
                                  help="Marca a nova conta como contabilizável (o saldo é calculado nas listagens)")
    conta_add_parser.add_argument(
        "--df", "--fechamento", help="Data de fechamento da conta")
    conta_add_parser.add_argument("nome", help="Nome da conta a ser criada")


def _make_conta_parser(parent_parser):
    conta_parser = parent_parser.add_parser("conta", help="Comandos de conta")
    subparsers = conta_parser.add_subparsers()

    _make_conta_list_parser(subparsers)
    _make_conta_add_parser(subparsers)


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


def locate_command_classes():
    import importlib

    command_module = importlib.import_module(".command", __package__)

    import pkgutil
    import inspect

    classes = []
    for importer, modulename, ispkg in pkgutil.iter_modules(command_module.__path__):
        submodule = importlib.import_module(
            "{}.command.{}".format(__package__, modulename))
        for class_name, clazz in inspect.getmembers(submodule, predicate=inspect.isclass):
            for method_name, method in inspect.getmembers(clazz, predicate=inspect.isfunction):
                if method_name == "make_parser":
                    classes.append(clazz)
                    break

    return classes


def make_command_parsers(command_classes, parent_parser):
    for command_class in command_classes:
        command_class.make_parser(parent_parser)


def parse_command_line():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    command_classes = locate_command_classes()

    make_command_parsers(command_classes, subparsers)

    _make_conta_parser(subparsers)

    _make_contrato_parser(subparsers)

    return parser.parse_args()


def main():
    args = parse_command_line()

    args.clazz().run(args)

if __name__ == '__main__':
    main()
