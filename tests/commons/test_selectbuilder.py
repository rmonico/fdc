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

        self.assertEqual('select table.rowid, table.field1, table.field2, table.field3 from table;', sql)

    def test_select_builder_with_where(self):
        builder = SelectBuilder(self.Table)

        sql = builder.build(where='field1 = ?')

        self.assertEqual('select table.rowid, table.field1, table.field2, table.field3 from table where field1 = ?;', sql)

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

    class Entity(RowWrapper):
        pass

    Entity.create_field('name')
    Entity.create_field('table', Table)

    class MasterEntity(RowWrapper):
        pass

    MasterEntity.create_field('mastername')
    MasterEntity.create_field('entity', Entity)


    def test_select_builder_should_generate_multiple_table_select(self):
        builder = SelectBuilder(self.MasterEntity)
        # import ipdb; ipdb.set_trace()
        sql = builder.build()

        fields = sql[:sql.index(' from')]
        from_clause = sql[sql.index('from '):]

        self.assertEqual('select masterentity.rowid, masterentity.mastername, entity.rowid, entity.name, table.rowid, table.field1, table.field2, table.field3', fields)
        self.assertEqual('from masterentity left join entity on (masterentity.entityid = entity.rowid) left join table on (entity.tableid = table.rowid);', from_clause)

    # TODO Teste do load com mais de uma tabela
    # TODO count(*)
    # TODO get_single
    # TODO order by
    # TODO Create table

    # TODO Depois fazer o mesmo esquema de entidade para o insert
    # TODO Para o update vai dar mais trabalho pois será necessário estender property


if __name__ == '__main__':
    unittest.main()
