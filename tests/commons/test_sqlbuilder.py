import unittest
from types import SimpleNamespace

from commons.abstract_dao import AbstractDao
from commons.rowwrapper import RowWrapper
from commons.sqlbuilder import TableDescriptor, InsertBuilder, SelectBuilder


class SQLBuilderTestCase(unittest.TestCase):
    def test_insert_builder(self):
        table_descriptor = TableDescriptor('table_name', 'field1', 'field2',
                                           'field3')
        builder = InsertBuilder(table_descriptor)
        sql = builder.build()

        self.assertEqual(
            'insert into table_name (field1, field2, field3) values (?, ?, ?);',
            sql)

    def test_get_fields_tuple(self):
        table_descriptor = TableDescriptor('table_name', 'field1', 'field2',
                                           'field3')

        entity = SimpleNamespace(field1='field 1 value',
                                 field2='value of field 2',
                                 field3='field 3')

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

        self.assertEqual(
            'select tablename.rowid, tablename.field1, tablename.field2, tablename.field3 from tablename;',
            sql)

    def test_select_builder_should_generate_multiple_table_select(self):
        class Referred(RowWrapper):
            pass

        Referred.create_field('value')

        class Entity(RowWrapper):
            pass

        Entity.create_field('nome')
        Entity.create_field('referred', Referred)

        builder = SelectBuilder(Entity)
        sql = builder.build()

        self.assertEqual(
            'select entity.rowid, entity.nome, referred.rowid, referred.value from entity left join referred on (entity.referredid = referred.rowid);',
            sql)

    def test_select_builder_with_where(self):
        class TableName(RowWrapper):
            pass

        TableName.create_field('field1')
        TableName.create_field('field2')
        TableName.create_field('field3')

        builder = SelectBuilder(TableName)

        sql = builder.build(where='field1 = ?')

        self.assertEqual(
            'select tablename.rowid, tablename.field1, tablename.field2, tablename.field3 from tablename where field1 = ?;',
            sql)

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

    def test_row_wrapper_should_load_row_with_references(self):
        class Referred(RowWrapper):
            pass

        Referred.create_field('value')

        class Entity(RowWrapper):
            pass

        Entity.create_field('nome')
        Entity.create_field('referred', Referred)

        row = (99, 'entity.nome', 98, 'referred.value')

        results = Entity.load([row])

        entity = results[0]

        self.assertEqual(99, entity.rowid)
        self.assertEqual('entity.nome', entity.nome)
        self.assertEqual(98, entity.referred.rowid)
        self.assertEqual('referred.value', entity.referred.value)

    def test_select_builder_make_selects_with_alias(self):
        class Entity(RowWrapper):
            pass

        Entity.alias = 'entity_name'
        Entity.create_field('nome')

        builder = SelectBuilder(Entity)
        sql = builder.build()

        self.assertEqual(
            'select entity_name.rowid, entity_name.nome from entity_name;',
            sql)


if __name__ == '__main__':
    unittest.main()
