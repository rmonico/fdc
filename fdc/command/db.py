#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class DBCommand(object):

    def make_parser(parent_parser):
        db_parser = parent_parser.add_parser("db", help="Database commands")
        subparsers = db_parser.add_subparsers()

        subparsers.add_parser(
            "init", help="Inicializa o banco de dados em fdc.db").set_defaults(clazz=DBInit)
        # subparsers.add_parser("restore", help="Restore fdc.dump to fdc.db").set_defaults(
        #     command=self.restore)
        # subparsers.add_parser(
        #     "dump", help="Dump fdc.db to fdc.dump").set_defaults(command=self.dump)

    def restore(self, args):
        # Usar iterdump do sqlite3
        print("in db restore {}".format(args))

    def dump(self, args):
        print("in db dump {}".format(args))


class DBInit(object):

    def run(self, args):
        print("in db init {}".format(args))
