#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sqlite3
from fdc import log


class Factory(object):

    def database_folder():
        import os

        return "{HOME}/.config/fdc".format(**os.environ)

    def database_path():
        # TODO CHeck this in other places (like environment variables, command
        # line switches, etc)
        return "{}/database.db".format(Factory.database_folder())

    def create_connection():
        import os

        os.makedirs(Factory.database_folder(), exist_ok=True)

        return sqlite3.connect(Factory.database_path())


def execute(sql, parameters):
    connection = Factory.create_connection()

    # FIXME Handle transaction

    cursor = connection.cursor()

    log.info("Executing", sql)
    log.info("  with parameters", parameters)

    cursor.execute(sql, parameters)

    cursor.close()

    connection.commit()

    connection.close()
