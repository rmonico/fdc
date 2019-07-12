#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from di_container.injector import di_container


class DBCommand(object):

    def root_parser_created_handler(self, root_parser):
        db_parser = root_parser.add_parser("db", help="Database commands")
        subparsers = db_parser.add_subparsers()

        subparsers.add_parser(
            "init", help="Inicializa o banco de dados em fdc.db").set_defaults(clazz=DBInit)

        subparsers.add_parser("restore", help="Restore fdc.dump to fdc.db").set_defaults(
            clazz=DBRestore)
        subparsers.add_parser(
            "dump", help="Dump fdc.db to fdc.dump").set_defaults(clazz=DBDump)


class DBInit(object):

    def __init__(self):
        self._configs = None

    def set_configs(self, configs):
        self._configs = configs

    def run(self, args):
        import os

        if os.path.exists(self._configs['db']['path']):
            os.remove(self._configs['db']['path'])

        connection = di_container.get_resource('connection')

        # TODO Move this to ContaCommand class (may that class should be
        # renamed)
        connection.executescript(
            "create table conta (nome text not null, contabilizavel boolean not null, fechamento date);")

        # FIXME Não armazenar monetários como float
        connection.executescript(
            "create table contrato (compra date not null, conta, total_parcelas integer, valor_parcela float, observacao text, foreign key(conta) references conta);")

        connection.executescript(
            "create table lancamento (debito date not null, compra date, valor float, valor_local float not null, origem, destino, parcela integer not null, observacao text not null, foreign key(origem) references conta, foreign key(destino) references conta);")

        # TODO Commit and handle errors


class DBRestore(object):

    def run(self, args):
        # Usar iterdump do sqlite3
        print("in db restore {}".format(args))


class DBDump(object):

    def run(self, args):
        print("in db dump {}".format(args))
