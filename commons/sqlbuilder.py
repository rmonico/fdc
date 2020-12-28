import inspect
from commons.rowwrapper import ColumnWrapper


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
        from_clause = self._get_from_clause()

        _fields = fields if fields else self._get_fields(self._entity_class)

        _where = ' where {}'.format(where) if where else ''

        return 'select {} from {}{};'.format(', '.join(_fields), from_clause, _where)

    def _get_from_clause(self):
        # TODO Create a method to return this
        main_table = self._entity_class.__name__.lower()
        from_clause = main_table

        parent_table = self._entity_class.__name__.lower()
        for _joined_table in self._get_class_complex_fields(self._entity_class):
            # FIXME Vai dar problema quando o builder não for RowWrapper
            # FIXME Prever a situação que houver mais de um nível de join (deve chamar esse bloco recursivamente)
            joined_table = getattr(self._entity_class, _joined_table)
            joined_table_name = joined_table._builder.__name__.lower()
            joined_table_field = joined_table._field_name

            from_clause += ' left join {0} on ({1}.{2} = {0}.rowid)'.format(joined_table_name, parent_table, joined_table_field)

        return from_clause

    @staticmethod
    def _get_fields(cls):
        mro = inspect.getmro(cls)
        fields = list()

        for cls in reversed(mro):
            # TODO Continuar mexendo aqui, precisa chamar o _get_fields recursivamente para montar os fields das tabelas joined
            fields.extend(SelectBuilder._get_class_fields(cls))

        return [cls.__name__.lower() + '.' + field for field in fields]

    @staticmethod
    def _get_class_fields(cls):
        d = cls.__dict__
        return [p for p in d if type(d[p]) == property]

    @staticmethod
    def _get_class_complex_fields(cls):
        d = cls.__dict__
        return [p for p in d if type(d[p]) == ColumnWrapper]

