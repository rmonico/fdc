#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from di_container.injector import Inject


class Conta(object):

    def __init__(self):
        self.nome = None
        self.contabilizavel = False
        self.fechamento = None


class ContaDao(object):

    def __init__(self):
        self._connection = Inject('database connection')

    @staticmethod
    def injectable_resource():
        return 'conta dao'

    @staticmethod
    def fields():
        return [{'name': 'nome'}, {'name': 'contabilizavel'}, {'name': 'fechamento'}]

    @staticmethod
    def _load_from_cursor(row):
        instance = Conta()

        for i, field in enumerate(ContaDao.fields()):
            value = row[i]
            setattr(instance, field['name'], value)

        return instance

    def list(self):
        cursor = self._connection.execute(
            "select {fields} from conta;".format(fields=", ".join(field['name'] for field in self.fields())))

        conta_list = []

        for row in cursor:
            conta = self._load_from_cursor(row)

            conta_list.append(conta)

        cursor.close()

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

        cursor = self._connection.execute(sql, fields)

        self._connection.commit()

        cursor.close()
