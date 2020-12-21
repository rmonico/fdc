import unittest

from commons.rowwrapper import RowWrapper
from commons.sqlbuilder import SelectBuilder


class SQLBuilderTestCase(unittest.TestCase):

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

        sql = builder.build(where='field1 = ?')

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
