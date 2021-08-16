# FIXME Acho que não precisa desse import
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

        return 'insert into {} ({}) values ({});'.format(
            table_name, self._fields_str(), values_mask)

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
        selectFields = fields or self._buildSelectFields(
            self._entity_class, self._entity_class.fields())

        from_clause = self._build_from_clause()

        result = f'select {", ".join(selectFields)} from {from_clause}'

        if where:
            result += ' where {}'.format(where)

        return result + ';'

    def _buildSelectFields(self, entity, fields):
        selectFields = list()

        for fieldName, referredFieldNames in fields.items():
            field = getattr(entity, fieldName)

            if type(field) == ColumnWrapper:
                selectFields.extend(
                    self._buildSelectFields(field._builder,
                                            referredFieldNames))
            else:
                selectFields.append(
                    f'{self._getTableNameFromClass(entity)}.{fieldName}')

        return selectFields

    def _build_from_clause(self):
        result = self._getTableNameFromClass(self._entity_class)

        result += self._do_build_from_clause(self._entity_class)

        return result

    def _do_build_from_clause(self, entityClass):
        result = ''

        entityName = self._getTableNameFromClass(entityClass)

        for fieldName, referredFieldnames in entityClass.fields().items():
            field = getattr(entityClass, fieldName)

            if type(field) == ColumnWrapper:
                # FIXME Vai dar problema quando o builder não for RowWrapper
                # FIXME Prever a situação que houver mais de um nível de join (deve chamar esse bloco recursivamente)
                referencedEntityClass = field._builder
                referencedEntityName = self._getTableNameFromClass(
                    referencedEntityClass)

                result += f' left join {referencedEntityName} on ({entityName}.{fieldName}id = {referencedEntityName}.rowid)'
                result += self._do_build_from_clause(referencedEntityClass)

        return result

    def _getTableNameFromClass(self, clss):
        if hasattr(clss, 'alias'):
            tableName = getattr(clss, 'alias')
        else:
            tableName = clss.__name__.lower()

        return tableName
