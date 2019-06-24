#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from datetime import date, datetime
from fdc import db, lanc


def _date_parser(s):
    return datetime.strptime(s, '%Y-%m-%d')


def _make_db_parser(parent_parser):
    db_parser = parent_parser.add_parser("db", help="Database commands")
    subparsers = db_parser.add_subparsers()

    subparsers.add_parser("init", help="Inicializa o banco de dados em fdc.db").set_defaults(func=db.Init())
    subparsers.add_parser("restore", help="Restore fdc.dump to fdc.db")
    subparsers.add_parser("dump", help="Dump fdc.db to fdc.dump")


def _make_lanc_add_parser(parent_parser):
    lanc_add_parser = parent_parser.add_parser("add", help="Cria um novo lançamento")
    lanc_add_parser.set_defaults(func=lanc.Add())

    lanc_add_parser.add_argument("-dd", "--data", type=_date_parser, default=date.today(), help="Data de débito da movimentação. Se omitido usa a data atual. Formato: AAAA-MM-DD")
    lanc_add_parser.add_argument("-dc", "--data-compra", type=_date_parser, help="Data da compra. Formato: AAAA-MM-DD")
    lanc_add_parser.add_argument("-vr", "--valor-reais", type=float, help="Valor em reais da movimentação")
    lanc_add_parser.add_argument("-pc", "--parcela-contrato", type=int, help="Parcela do contrato")
    lanc_add_parser.add_argument("-o", "--observacao", help="Observações")
    lanc_add_parser.add_argument("origem", help="Conta de origem")
    lanc_add_parser.add_argument("destino", help="Conta de destino")
    lanc_add_parser.add_argument("valor", type=float, help="Valor (na moeda da movimentação)")


def _make_lanc_parser(parent_parser):
    lanc_parser = parent_parser.add_parser("lanc", help="Lançamento commands")
    subparsers = lanc_parser.add_subparsers()

    subparsers.add_parser("list", help="List lançamentos")

    _make_lanc_add_parser(subparsers)


def _make_conta_list_parser(parent_parser):
    conta_list_parser = parent_parser.add_parser("list", help="Lista as contas existentes")


def _make_conta_add_parser(parent_parser):
    conta_add_parser = parent_parser.add_parser("add", help="Adiciona uma nova conta")

    conta_add_parser.add_argument("-c", "--contabilizavel", action="store_true", help="Marca a nova conta como contabilizável (o saldo é calculado nas listagens)")
    conta_add_parser.add_argument("--df", "--fechamento", help="Data de fechamento da conta")
    conta_add_parser.add_argument("nome", help="Nome da conta a ser criada")


def _make_conta_parser(parent_parser):
    conta_parser = parent_parser.add_parser("conta", help="Comandos de conta")
    subparsers = conta_parser.add_subparsers()

    _make_conta_list_parser(subparsers)
    _make_conta_add_parser(subparsers)


def _make_contrato_list_parser(parent_parser):
    contrato_list_parser = parent_parser.add_parser("list", help="Lista os contratos existentes")


def _make_contrato_add_parser(parent_parser):
    contrato_add_parser = parent_parser.add_parser("add", help="Adiciona um novo contrato")

    contrato_add_parser.add_argument("data-compra", type=_date_parser, help="Data da compra. Formato: AAAA-MM-DD")
    contrato_add_parser.add_argument("conta", help="Conta associada")
    contrato_add_parser.add_argument("total-parcelas", type=int, help="Total de parcelas")
    contrato_add_parser.add_argument("-v", "--valor-parcela", type=float, help="Valor da parcela")
    contrato_add_parser.add_argument("-o", "--observacao", help="Observações")


def _make_contrato_parser(parent_parser):
    contrato_parser = parent_parser.add_parser("contrato", help="Comandos de contrato")
    subparsers = contrato_parser.add_subparsers()

    _make_contrato_list_parser(subparsers)

    _make_contrato_add_parser(subparsers)


def parse_command_line():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    _make_db_parser(subparsers)

    _make_lanc_parser(subparsers)

    _make_conta_parser(subparsers)

    _make_contrato_parser(subparsers)

    return parser.parse_args()


def main():
    args = parse_command_line()

    args.func.run(args)

if __name__ == '__main__':
    main()
