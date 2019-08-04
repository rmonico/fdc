import unittest

from commons.sqlbuilder import TableDescriptor, InsertBuilder, SelectBuilder
from types import SimpleNamespace


class SQLBuilderTestCase(unittest.TestCase):

    def test_insert_builder(self):
        table_descriptor = TableDescriptor('table_name', 'field1', 'field2', 'field3')
        builder = InsertBuilder(table_descriptor)
        sql = builder.build()

        self.assertEqual('insert into table_name (field1, field2, field3) values (?, ?, ?);', sql)

    def test_get_fields_tuple(self):
        table_descriptor = TableDescriptor('table_name', 'field1', 'field2', 'field3')

        entity = SimpleNamespace(field1='field 1 value', field2='value of field 2', field3='field 3')

        field1, field2, field3 = table_descriptor.get_fields_tuple(entity)

        self.assertEqual('field 1 value', field1)
        self.assertEqual('value of field 2', field2)
        self.assertEqual('field 3', field3)

    def test_select_builder(self):
        table_descriptor = TableDescriptor('table_name', 'field1', 'field2', 'field3')
        builder = SelectBuilder(table_descriptor)
        sql = builder.build()

        self.assertEqual('select field1, field2, field3 from table_name;', sql)


if __name__ == '__main__':
    unittest.main()
