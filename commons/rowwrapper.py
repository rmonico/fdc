import logging

logger = logging.getLogger(__name__)


class ColumnWrapper(property):

    def __init__(self, row_class, field_name, field_index, builder, consumed_itens):
        super().__init__(self)
        # self.row_class = row_class
        self._field_name = field_name
        self._field_index = field_index
        self._builder = builder
        # self._consumed_itens = consumed_itens

    def __call__(self, row_wrapper):
        return row_wrapper._get_property_value(self)


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
        if not builder:
            field_index = int(cls._field_count)
            p = property(lambda self: self._row[self._offset + field_index])
        else:
            p = ColumnWrapper(cls, name, cls._field_count, builder, consumed_items)
        setattr(cls, name, p)
        cls._field_count += consumed_items if consumed_items else getattr(builder, '_field_count', 1)

    @classmethod
    def load(cls, cursor):
        return [cls(row, 0) for row in cursor]

    @classmethod
    def fields(clss):
        # FIXME Will have a problem when creating fields after call this
        if not hasattr(clss, '_fields_cache'):
            clss._fields_cache = clss._fields()

        return clss._fields_cache

    @classmethod
    def _fields(cls):
        fields = dict()

        fields.update(cls._fields_from_super_class())

        for name, prop in cls.__dict__.items():
            if not isinstance(prop, property):
                continue

            fields[name] = None

            if type(prop) == ColumnWrapper:
                # FIXME Avoid recursion on self-referred entities
                fields[name] = prop._builder._fields()

        return fields

    @classmethod
    def _fields_from_super_class(current_class):
        super_class = current_class.mro()[1]

        return [] if super_class == object else super_class._fields()

    def _get_property_value(self, property):
        if property._field_index not in self._referenced_fields:
            self._referenced_fields[property._field_index] = property._builder(self._row, property._field_index)

        return self._referenced_fields[self._offset + property._field_index]


RowWrapper.create_field('rowid')
