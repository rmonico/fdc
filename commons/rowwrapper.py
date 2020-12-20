import logging


logger = logging.getLogger(__name__)

class RowWrapper(object):
    _field_count = 0

    def __init__(self, row, offset=0):
        self._row = row
        self._offset = offset
        self._referenced_fields = dict()

    @classmethod
    def create_field(cls, name, builder = None, consumed_items = None):
        logger.debug('creating field "{}" on class "{}" with index {} of class "{}", consuming {} items'.format(name, str(cls), cls._field_count, builder, consumed_items))
        field_index = int(cls._field_count)
        p = property(lambda self: self._field_getter(field_index, builder))
        setattr(cls, name, p)
        cls._field_count += consumed_items if consumed_items else getattr(builder, '_field_count', 1)

    def _field_getter(self, field, builder):
        if builder:
            if not field in self._referenced_fields:
                self._referenced_fields[field] = builder(self._row, field)

            return self._referenced_fields[self._offset + field]

        logger.debug('getting field index {} with offset {}'.format(field, self._offset))
        return self._row[self._offset + field]

    @classmethod
    def load(cls, cursor):
        return [ cls(row, 0) for row in cursor ]

RowWrapper.create_field('rowid')
