#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import connection
from fdc.parsers.date_parser import date_parser
from datetime import date
from .tableprinter import TablePrinter


class ContaCommand(object):

    def make_parser(parent_parser):
        conta_parser = parent_parser.add_parser(
            "conta", help="Comandos de conta")
        subparsers = conta_parser.add_subparsers()

        ContaCommand._make_conta_list_parser(subparsers)
        ContaCommand._make_conta_add_parser(subparsers)

    def _make_conta_list_parser(parent_parser):
        conta_list_parser = parent_parser.add_parser(
            "list", help="Lista as contas existentes").set_defaults(clazz=ContaList)

    def _make_conta_add_parser(parent_parser):
        conta_add_parser = parent_parser.add_parser(
            "add", help="Adiciona uma nova conta")

        conta_add_parser.set_defaults(clazz=ContaAdd)

        conta_add_parser.add_argument("-c", "--contabilizavel", default=False, action="store_true",
                                      help="Marca a nova conta como contabilizável (o saldo é calculado nas listagens)")
        conta_add_parser.add_argument(
            "--df", "--fechamento", help="Data de fechamento da conta")
        conta_add_parser.add_argument(
            "nome", help="Nome da conta a ser criada")


class ContaList(object):

    def run(self, args):
        fields = "nome", "contabilizavel", "fechamento"

        result_set = connection.execute(
            "select {fields} from conta;".format(fields=", ".join(fields)))

        printer = TablePrinter(fields, result_set)

        printer.print()


class ContaAdd(object):

    def run(self, args):
        # TODO Extract these code to a InsertBuilder class (maybe on connection
        # module, not sure yet)
        fields = args.nome, args.contabilizavel
        field_names = ["nome", "contabilizavel"]
        value_mask = "?, ?"

        if hasattr(args, "fechamento"):
            fields += args.fechamento,
            field_names += ["fechamento"]
            value_mask += ", ?"

        sql = "insert into conta ({fields}) values ({value_mask});".format(
            fields=", ".join(field_names), value_mask=value_mask)

        connection.execute(sql, fields, True)
