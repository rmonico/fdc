class TableDescriptor(object):

    def __init__(self, table_name, *fields):
        self.table_name = table_name
        self.fields = list(fields)

    def create_field_attributes(self, entity, **kwargs):
        for field in self.fields:
            setattr(entity, field, kwargs.get(field))


class SQLBuilder(object):

    def __init__(self, table_descriptor):
        self._table_descriptor = table_descriptor

    def _fields_str(self):
        return ', '.join(self._get_fields())

    def _get_fields(self):
        return self._table_descriptor.fields


class InsertBuilder(SQLBuilder):

    def __init__(self, table_descriptor):
        super().__init__(table_descriptor)

    def build(self):
        table_name = self._table_descriptor.table_name
        values_mask = ', '.join('?' * len(self._get_fields()))

        return 'insert into {} ({}) values ({});'.format(table_name, self._fields_str(), values_mask)

    def _get_fields(self):
        fields = tuple()

        for field in super()._get_fields():
            if field == 'rowid':
                continue

            fields += field,

        return fields


class SelectBuilder(SQLBuilder):

    def __init__(self, table_descriptor):
        super().__init__(table_descriptor)
        self._fields = tuple()
        self.where = ''

    def build(self):
        table_name = self._table_descriptor.table_name

        where = ' where ' + self.where if self.where and self.where != '' else ''

        return 'select {} from {}{};'.format(self._fields_str(), table_name, where)

    def fields(self, *fields):
        self._fields = fields

        return self

    def _get_fields(self):
        return self._fields if len(self._fields) > 0 else self._table_descriptor.fields
