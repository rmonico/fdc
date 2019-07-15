#!/usr/bin/env python3
# -*- coding: utf-8 -*-

_fields = "nome", "contabilizavel", "fechamento"


class Conta(object):

    def __init__(self, conta_row):
        for field in _fields:
            setattr(self, '_' + field, conta_row[field])


class ContaDao(object):

    def __init__(self):
        self._connection = None

    @staticmethod
    def injectable_resource():
        return 'conta_dao'

    def set_connection(self, connection):
        self._connection = connection

    def list(self):
        cursor = self._connection.execute(
            "select {fields} from conta;".format(fields=", ".join(_fields)))

        conta_list = []

        for row in cursor:
            conta = Conta(conta_row=row)

            conta_list.append(conta)

        return conta_list

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
