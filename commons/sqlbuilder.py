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


class SelectBuilder(object):

    def __init__(self, entity_class):
        super().__init__()
        self._entity_class = entity_class

    def build(self, where: str = None, fields: list = None):
        # TODO Create a method to return this
        table_name = self._entity_class.__name__.lower()

        _fields = fields if fields else self._get_fields()

        _where = ' where {}'.format(where) if where else ''

        return 'select {} from {}{};'.format(', '.join(_fields), table_name, _where)

    def _get_fields(self):
        d = self._entity_class.__dict__
        return [p for p in d if type(d[p]) == property]
