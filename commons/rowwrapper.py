import logging


logger = logging.getLogger(__name__)

class RowWrapper(object):
    _field_count = 0

    def __init__(self, row, offset=0):
        self._row = row
        self._offset = offset
        self._referenced_fields = dict()

    @classmethod
    def _create_field(cls, field_name, field_class = None):
        logger.debug('creating field "{}" on class "{}" with index {} of class "{}"'.format(field_name, str(cls), cls._field_count, field_class))
        field_index = int(cls._field_count)
        p = property(lambda self: self._field_getter(field_index, field_class))
        setattr(cls, field_name, p)
        cls._field_count += field_class._field_count if field_class else 1

    def _field_getter(self, field, field_class):
        if field_class:
            if not field in self._referenced_fields:
                self._referenced_fields[field] = field_class(self._row, field)

            return self._referenced_fields[self._offset + field]

        logger.debug('getting field index {} with offset {}'.format(field, self._offset))
        return self._row[self._offset + field]

    @staticmethod
    def load(cursor, row_class):
        return [ row_class(row, 0) for row in cursor ]

RowWrapper._create_field('rowid')
