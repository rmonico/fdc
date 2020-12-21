import unittest
from types import SimpleNamespace

from commons.abstract_dao import AbstractDao
from commons.sqlbuilder import TableDescriptor, InsertBuilder


class InsertBuilderTestCase(unittest.TestCase):

    def test_insert_builder(self):
        table_descriptor = TableDescriptor('table_name', 'field1', 'field2', 'field3')
        builder = InsertBuilder(table_descriptor)
        sql = builder.build()

        self.assertEqual('insert into table_name (field1, field2, field3) values (?, ?, ?);', sql)

    def test_get_fields_tuple(self):
        table_descriptor = TableDescriptor('table_name', 'field1', 'field2', 'field3')

        entity = SimpleNamespace(field1='field 1 value', field2='value of field 2', field3='field 3')

        builder = AbstractDao(object, table_descriptor)

        field1, field2, field3 = builder._get_field_values(entity)

        self.assertEqual('field 1 value', field1)
        self.assertEqual('value of field 2', field2)
        self.assertEqual('field 3', field3)
