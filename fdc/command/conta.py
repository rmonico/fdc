#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from di_container.controller import controller
from fdc.dao.conta import Conta, ContaDao


class ContaCommand(object):

    def root_parser_created_handler(self, root_parser):
        conta_parser = root_parser.add_parser(
            "conta", aliases=['c', 'ct', 'cta'], help="Comandos de conta")
        subparsers = conta_parser.add_subparsers()

        controller.event('conta_parser_created', conta_parser=subparsers)

        ContaCommand._make_conta_add_parser(subparsers)

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


class ContaAdd(object):

    def run(self, args):
        conta = Conta()

        conta.nome = args.nome
        conta.contabilizavel = args.contabilizavel
        if hasattr(args, "fechamento"):
            conta.fechamento = args.fechamento

        dao = ContaDao()

        dao.insert(conta)
