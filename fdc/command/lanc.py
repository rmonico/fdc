#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import connection
from fdc.parsers.date_parser import date_parser
from datetime import date


class LancCommand(object):

    def make_parser(parent_parser):
        lanc_parser = parent_parser.add_parser(
            "lanc", help="Lançamento commands")
        subparsers = lanc_parser.add_subparsers()

        subparsers.add_parser("list", help="List lançamentos")

        LancCommand._make_lanc_add_parser(subparsers)

    def _make_lanc_add_parser(parent_parser):
        lanc_add_parser = parent_parser.add_parser(
            "add", help="Cria um novo lançamento")
        lanc_add_parser.set_defaults(clazz=LancAdd)

        lanc_add_parser.add_argument("-dd", "--data", type=date_parser, default=date.today(
        ), help="Data de débito da movimentação. Se omitido usa a data atual. Formato: AAAA-MM-DD")
        lanc_add_parser.add_argument(
            "-dc", "--data-compra", type=date_parser, help="Data da compra. Formato: AAAA-MM-DD")
        lanc_add_parser.add_argument(
            "-vr", "--valor-reais", type=float, help="Valor em reais da movimentação")
        lanc_add_parser.add_argument(
            "-pc", "--parcela-contrato", type=int, help="Parcela do contrato")
        lanc_add_parser.add_argument("-o", "--observacao", help="Observações")
        lanc_add_parser.add_argument("origem", help="Conta de origem")
        lanc_add_parser.add_argument("destino", help="Conta de destino")
        lanc_add_parser.add_argument(
            "valor", type=float, help="Valor (na moeda da movimentação)")


class LancAdd(object):

    def run(self, args):
        print("TODO")
