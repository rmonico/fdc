#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from .parsers.date_parser import date_parser
from .classvisitor import ClassVisitor, has_method


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


def parse_command_line():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    visitor = ClassVisitor("command", lambda clazz: has_method(clazz, 'make_parser'))

    visitor.visit(lambda command_class: command_class.make_parser(subparsers))

    _make_contrato_parser(subparsers)

    return parser.parse_args()


def main():
    args = parse_command_line()

    args.clazz().run(args)

if __name__ == '__main__':
    main()
