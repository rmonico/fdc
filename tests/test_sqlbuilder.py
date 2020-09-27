import unittest
from types import SimpleNamespace
from commons.abstract_dao import AbstractDao
from commons.sqlbuilder import TableDescriptor, InsertBuilder, SelectBuilder


class SQLBuilderTestCase(unittest.TestCase):

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

    def test_select_builder(self):
        table_descriptor = TableDescriptor('table_name', 'field1', 'field2', 'field3')
        builder = SelectBuilder(table_descriptor)
        sql = builder.build()

        self.assertEqual('select field1, field2, field3 from table_name;', sql)

    def test_select_builder_with_where(self):
        table_descriptor = TableDescriptor('table_name', 'field1', 'field2', 'field3')
        builder = SelectBuilder(table_descriptor)
        builder.where = 'field1 = ?'

        sql = builder.build()

        self.assertEqual('select field1, field2, field3 from table_name where field1 = ?;', sql)

    def test_select_builder_with_fields(self):
        table_descriptor = TableDescriptor('table_name', 'field1', 'field2', 'field3')
        builder = SelectBuilder(table_descriptor)
        builder.fields('field1', 'field2')

        sql = builder.build()

        self.assertEqual('select field1, field2 from table_name;', sql)

    def test_abstract_dao_load_row(self):
        table_descriptor = TableDescriptor('table_name', 'field1', 'field2', 'field3')
        dao = AbstractDao(object, table_descriptor)

        row = 'field 1 value', 'value of field 2', 'field 3'

        entity = dao._load_row(row)

        self.assertEqual('field 1 value', entity.field1)
        self.assertEqual('value of field 2', entity.field2)
        self.assertEqual('field 3', entity.field3)


if __name__ == '__main__':
    unittest.main()
