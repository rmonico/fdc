#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sqlite3
from fdc import log


# TODO Move these methods to module
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


def execute(sql, parameters=None, commit_and_close=False):
    connection = Factory.create_connection()

    # FIXME Handle transaction

    cursor = connection.cursor()

    log.info("Executing", sql)

    if parameters:
        log.info("  with parameters", parameters)
        result = cursor.execute(sql, parameters)
    else:
        result = cursor.execute(sql)

    if commit_and_close:
        cursor.close()
        connection.commit()
        connection.close()

    return result
