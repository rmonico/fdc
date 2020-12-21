import unittest

from commons.rowwrapper import RowWrapper
from commons.sqlbuilder import SelectBuilder


class SelectBuilderTestCase(unittest.TestCase):
    class Table(RowWrapper):
        pass

    Table.create_field('field1')
    Table.create_field('field2')
    Table.create_field('field3')

    def test_select_builder_should_generate_single_table_select(self):
        builder = SelectBuilder(self.Table)
        sql = builder.build()

        self.assertEqual('select field1, field2, field3 from table;', sql)

    def test_select_builder_with_where(self):
        builder = SelectBuilder(self.Table)

        sql = builder.build(where='field1 = ?')

        self.assertEqual('select field1, field2, field3 from table where field1 = ?;', sql)

    def test_select_builder_with_fields(self):
        builder = SelectBuilder(self.Table)

        sql = builder.build(fields=['field1', 'field2'])

        self.assertEqual('select field1, field2 from table;', sql)

    def test_row_wrapper_load_row(self):
        row = (99, 'field 1 value', 'value of field 2', 'field 3')

        results = self.Table.load([row])

        entity = results[0]

        self.assertEqual(99, entity.rowid)
        self.assertEqual('field 1 value', entity.field1)
        self.assertEqual('value of field 2', entity.field2)
        self.assertEqual('field 3', entity.field3)


if __name__ == '__main__':
    unittest.main()
