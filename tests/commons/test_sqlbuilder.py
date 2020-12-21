import unittest
from types import SimpleNamespace

from commons.abstract_dao import AbstractDao
from commons.rowwrapper import RowWrapper
from commons.sqlbuilder import TableDescriptor, InsertBuilder, SelectBuilder


class SQLBuilderTestCase(unittest.TestCase):

    @unittest.skip
    def test_insert_builder(self):
        table_descriptor = TableDescriptor('table_name', 'field1', 'field2', 'field3')
        builder = InsertBuilder(table_descriptor)
        sql = builder.build()

        self.assertEqual('insert into table_name (field1, field2, field3) values (?, ?, ?);', sql)

    @unittest.skip
    def test_get_fields_tuple(self):
        table_descriptor = TableDescriptor('table_name', 'field1', 'field2', 'field3')

        entity = SimpleNamespace(field1='field 1 value', field2='value of field 2', field3='field 3')

        builder = AbstractDao(object, table_descriptor)

        field1, field2, field3 = builder._get_field_values(entity)

        self.assertEqual('field 1 value', field1)
        self.assertEqual('value of field 2', field2)
        self.assertEqual('field 3', field3)

    def test_select_builder_should_generate_single_table_select(self):
        class TableName(RowWrapper):
            pass

        TableName.create_field('field1')
        TableName.create_field('field2')
        TableName.create_field('field3')

        builder = SelectBuilder(TableName)
        sql = builder.build()

        self.assertEqual('select field1, field2, field3 from tablename;', sql)

    def test_select_builder_with_where(self):
        class TableName(RowWrapper):
            pass

        TableName.create_field('field1')
        TableName.create_field('field2')
        TableName.create_field('field3')

        builder = SelectBuilder(TableName)

        sql = builder.build(where = 'field1 = ?')

        self.assertEqual('select field1, field2, field3 from tablename where field1 = ?;', sql)

    def test_select_builder_with_fields(self):
        class TableName(RowWrapper):
            pass

        TableName.create_field('field1')
        TableName.create_field('field2')
        TableName.create_field('field3')

        builder = SelectBuilder(TableName)

        sql = builder.build(fields=['field1', 'field2'])

        self.assertEqual('select field1, field2 from tablename;', sql)

    def test_row_wrapper_load_row(self):
        class TableName(RowWrapper):
            pass

        TableName.create_field('field1')
        TableName.create_field('field2')
        TableName.create_field('field3')

        row = (99, 'field 1 value', 'value of field 2', 'field 3')

        results = TableName.load([row])

        entity = results[0]

        self.assertEqual(99, entity.rowid)
        self.assertEqual('field 1 value', entity.field1)
        self.assertEqual('value of field 2', entity.field2)
        self.assertEqual('field 3', entity.field3)


if __name__ == '__main__':
    unittest.main()
