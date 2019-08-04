class TableDescriptor(object):

    def __init__(self, table_name, *fields):
        self.table_name = table_name
        self.fields = list(fields)

    def get_fields_tuple(self, entity):
        t = ()

        for field in self.fields:
            t += getattr(entity, field, None),

        return t


class InsertBuilder(object):

    def __init__(self, table_descriptor):
        self._table_descriptor = table_descriptor

    def build(self):
        table_name = self._table_descriptor.table_name
        fields = ', '.join(self._table_descriptor.fields)
        values_mask = ', '.join('?' * len(self._table_descriptor.fields))

        return 'insert into {} ({}) values ({});'.format(table_name, fields, values_mask)
