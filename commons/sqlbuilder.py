class TableDescriptor(object):

    def __init__(self, table_name, *fields):
        self.table_name = table_name
        self.fields = list(fields)

    def get_fields_tuple(self, entity):
        t = ()

        for field in self.fields:
            t += getattr(entity, field, None),

        return t


class SQLBuilder(object):

    def __init__(self, table_descriptor):
        self._table_descriptor = table_descriptor
        self._fields = None

    def _fields_str(self):
        return ', '.join(self._fields if self._fields else self._table_descriptor.fields)


class InsertBuilder(SQLBuilder):

    def __init__(self, table_descriptor):
        super().__init__(table_descriptor)

    def build(self):
        table_name = self._table_descriptor.table_name
        values_mask = ', '.join('?' * len(self._table_descriptor.fields))

        return 'insert into {} ({}) values ({});'.format(table_name, self._fields_str(), values_mask)


class SelectBuilder(SQLBuilder):

    def __init__(self, table_descriptor):
        super().__init__(table_descriptor)
        self._where = list()

    def build(self):
        table_name = self._table_descriptor.table_name

        where = self._make_where()

        return 'select {} from {}{};'.format(self._fields_str(), table_name, where)

    def _make_where(self):
        if len(self._where) == 0:
            return ''

        return ' where ' + 'and '.join(self._where)

    def where(self, clause):
        self._where.append(clause)

    def fields(self, *fields):
        self._fields = list(fields)
