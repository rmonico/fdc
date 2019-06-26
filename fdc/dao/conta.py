#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fdc.command import connection

class Conta():
    pass


class ContaDao():

    def insert(self, conta):
        # TODO Extract these code to a InsertBuilder class (maybe on connection
        # module, not sure yet)
        fields = conta.nome, conta.contabilizavel
        field_names = ["nome", "contabilizavel"]
        value_mask = "?, ?"

        if hasattr(conta, "fechamento"):
            fields += conta.fechamento,
            field_names += ["fechamento"]
            value_mask += ", ?"

        sql = "insert into conta ({fields}) values ({value_mask});".format(
            fields=", ".join(field_names), value_mask=value_mask)

        connection.execute(sql, fields, True)
