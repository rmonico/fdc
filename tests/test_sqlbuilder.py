import unittest

from commons.sqlbuilder import TableDescriptor, InsertBuilder


class MyTestCase(unittest.TestCase):

    def test_something(self):
        table_descriptor = TableDescriptor('table_name', 'field1', 'field2', 'field3')
        builder = InsertBuilder()
        sql = builder.build(table_descriptor)

        self.assertEqual('insert into table_name (field1, field2, field3) values (?, ?, ?);', sql)


if __name__ == '__main__':
    unittest.main()
