#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fdc.command.tableprinter import TablePrinter


class ContaListCommand(object):

    def __init__(self):
        self._dao = None

    def set_conta_dao(self, conta_dao):
        self._dao = conta_dao

    @staticmethod
    def conta_parser_created_handler(conta_parser):
        conta_parser.add_parser("list", aliases=['l', 'ls'], help="Lista as contas existentes").set_defaults(
            event='conta_list_command')

    def conta_list_command_handler(self, args):
        contas = self._dao.list()

        return 'ok', contas

    def conta_list_command_ok_handler(self, contas):
        printer = TablePrinter(self._dao.fields(), contas)

        printer.print()
