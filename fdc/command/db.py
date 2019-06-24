#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import connection


class DBCommand(object):

    def make_parser(parent_parser):
        db_parser = parent_parser.add_parser("db", help="Database commands")
        subparsers = db_parser.add_subparsers()

        subparsers.add_parser(
            "init", help="Inicializa o banco de dados em fdc.db").set_defaults(clazz=DBInit)

        subparsers.add_parser("restore", help="Restore fdc.dump to fdc.db").set_defaults(
            command=DBRestore)
        subparsers.add_parser(
            "dump", help="Dump fdc.db to fdc.dump").set_defaults(command=DBDump)


class DBInit(object):

    def run(self, args):
        import os

        os.remove(connection.Factory.database_path())

        conn = connection.Factory.create()

        conn.executescript(
            "create table conta (nome text not null, contabilizavel boolean not null, fechamento date);")

        # FIXME Não armazenar monetários como float
        conn.executescript(
            "create table contrato (compra date not null, conta, total_parcelas integer, valor_parcela float, observacao text, foreign key(conta) references conta);")

        conn.executescript("create table lancamento (debito date not null, compra date, valor float, valor_local float not null, origem, destino, parcela integer not null, observacao text not null, foreign key(origem) references conta, foreign key(destino) references conta);")


class DBRestore(object):

    def run(self, args):
        # Usar iterdump do sqlite3
        print("in db restore {}".format(args))


class DBDump(object):

    def run(self, args):
        print("in db dump {}".format(args))
