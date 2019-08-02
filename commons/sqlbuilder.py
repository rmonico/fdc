class TableDescriptor(object):
    def __init__(self, table_name, *fields):
        self.table_name = table_name
        self.fields = list(fields)


class InsertBuilder(object):

    def build(self, table_descriptor):
        table_name = table_descriptor.table_name
        fields = ', '.join(table_descriptor.fields)
        values_mask = ', '.join('?' * len(table_descriptor.fields))

        return 'insert into {} ({}) values ({});'.format(table_name, fields, values_mask)
