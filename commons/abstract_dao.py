from types import SimpleNamespace

from commons.sqlbuilder import SelectBuilder, InsertBuilder
from di_container.injector import Inject


class AbstractDao(object):

    def __init__(self, entity_class, metadata):
        self._connection = Inject('database connection')
        self._logger = Inject('logger')
        self._entity_class = entity_class
        self._metadata = metadata

    def new_builder(self, kind):
        if kind == 'SELECT':
            return SelectBuilder(self._metadata)
        else:
            return None

    def get_single(self, where=None, *values):
        list = self.list(where, *values)

        return list[0] if len(list) > 0 else None

    def list(self, where=None, *values):
        cursor = self._create_select_cursor((), where, *values)

        entity_list = self._load_cursor(cursor)

        cursor.close()

        return entity_list

    def exists(self, where, *values):
        cursor = self._create_select_cursor(('count(*)',), where, *values)

        count = cursor.fetchone()[0]

        return count > 0

    def _create_select_cursor(self, fields=(), where=None, *values):
        builder = self.new_builder('SELECT')

        builder.where = where

        builder.fields(*fields) if len(fields) > 0 else None

        query = builder.build()

        return self._connection.execute(query, values)

    def _load_cursor(self, cursor):
        entity_list = []
        for row in cursor:
            entity = self._load_row(row)

            entity_list.append(entity)
        return entity_list

    def _load_row(self, row):
        entity_values = {}

        for i, field_name in enumerate(self._metadata.fields):
            value = row[i]

            entity_values[field_name] = value

        return SimpleNamespace(**entity_values)

    def insert(self, entity):
        builder = InsertBuilder(self._metadata)

        sql = builder.build()

        values = self._get_field_values(entity)

        self._logger.debug('Running "{}" with values "{}"', sql, values)

        self._connection.execute(sql, values)

        self._connection.commit()

    def _get_field_values(self, entity):
        t = ()

        for field in self._metadata.fields:
            if field == 'rowid':
                continue

            value = getattr(entity, field, None)

            if hasattr(value, 'rowid'):
                t += value.rowid,
            else:
                t += value,

        return t
