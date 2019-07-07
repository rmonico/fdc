#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import date
from .tableprinter import TablePrinter
from fdc.dao.conta import Conta, ContaDao

class ContaCommand(object):

    def root_parser_created_handler(self, root_parser):
        conta_parser = root_parser.add_parser(
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
        conta = Conta()

        conta.nome = args.nome
        conta.contabilizavel = args.contabilizavel
        if hasattr(args, "fechamento"):
            conta.fechamento = args.fechamento

        dao = ContaDao()

        dao.insert(conta)
