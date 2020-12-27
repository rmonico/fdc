import logging

logger = logging.getLogger(__name__)


class ColumnWrapper(property):

    def __init__(self, row_class, field_name, field_index, builder, consumed_itens):
        super().__init__(self)
        # self._row_class = row_class
        # self._field_name = field_name
        self._field_index = field_index
        self._builder = builder
        # self._consumed_itens = consumed_itens

    def __call__(self, row_wrapper):
        if self._builder:
            if self._field_index not in row_wrapper._referenced_fields:
                row_wrapper._referenced_fields[self._field_index] = self._builder(row_wrapper._row, self._field_index)

            return row_wrapper._referenced_fields[row_wrapper._offset + self._field_index]

        logger.debug('getting field index {} with offset {}'.format(self._field_index, row_wrapper._offset))
        return row_wrapper._row[row_wrapper._offset + self._field_index]


class RowWrapper(object):
    _field_count = 0

    def __init__(self, row, offset=0):
        self._row = row
        self._offset = offset
        self._referenced_fields = dict()

    @classmethod
    def create_field(cls, name, builder=None, consumed_items=None):
        logger.debug(
            'creating field "{}" on class "{}" with index {} of class "{}", consuming {} items'.format(name, str(cls),
                                                                                                       cls._field_count,
                                                                                                       builder,
                                                                                                       consumed_items))
        p = ColumnWrapper(cls, name, cls._field_count, builder, consumed_items)
        setattr(cls, name, p)
        cls._field_count += consumed_items if consumed_items else getattr(builder, '_field_count', 1)

    @classmethod
    def load(cls, cursor):
        return [cls(row, 0) for row in cursor]


RowWrapper.create_field('rowid')
