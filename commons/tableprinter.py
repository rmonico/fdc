import sys

from converters import currency
from converters import date


class TablePrinterFactory(object):
    """
    Creates 'TablePrinter' objects.

    The method 'add' create the new column and return it. Note its possible to add a custom column not created by this
    class.

    At least 'title' and 'getter' must be specified before call 'add'.

    The '<type>_column' methods create column with pre-formatted types.

    The 'of_attr' method assign title and getter for a object property. Its also possible pass 'property.subproperty'
    to get the value of a property of a embedded object.

    The 'create' method return the 'TablePrinter' object.
    Instances of this class can be reused.
    """

    def __init__(self):
        self._formatter = None
        self._title = None
        self._getter = None

        self._reset()

    def date_column(self):
        self._formatter = date.format
        return self

    def string_column(self):
        self._formatter = lambda value: str(value)
        return self

    def currency_column(self):
        self._formatter = currency.format
        return self

    # FIXME default_value should be in another method
    def of_attr(self, attribute, default_value=None):
        attr_path = attribute.split('.')
        self.title(attr_path[0].capitalize())

        def _get_sub_attr(data, attr):
            new_data = getattr(data, attr[0])
            return new_data if len(attr) == 1 else _get_sub_attr(new_data, attr[1:])

        self.getter(lambda row, data: _get_sub_attr(row, attr_path))

        return self

    def title(self, title: str):
        self._title = title
        return self

    def getter(self, getter):
        self._getter = getter
        return self

    def formatter(self, formatter):
        self._formatter = formatter
        return self

    def add(self, _column=None):
        if _column:
            self._columns.append(_column)
        else:
            column = self._create_column()
            self._columns.append(column)

        self._reset_column()

        return _column if _column else self._columns[-1]

    def _create_column(self):
        if self._formatter:
            return Column(self._title, self._getter, self._formatter)
        else:
            return Column(self._title, self._getter)

    def _reset_column(self):
        self._title = None
        self._getter = None
        self._formatter = None

    def create(self):
        columns = self._columns
        self._reset()
        return TablePrinter(columns)

    def _reset(self):
        self._columns = list()
        self._reset_column()


class TablePrinter(object):

    def __init__(self, columns):
        self._columns = columns

    def print(self, data, output=sys.stdout):
        raw_data = self._load_and_format_data(data)

        column_widths = self._calculate_column_widths(raw_data)

        self._print(raw_data, column_widths, output)

    def _load_and_format_data(self, data):
        raw_data = [self._make_title_row()]

        for row in data:
            raw_row = []
            for column in self._columns:
                raw_value = column.get_value(row, data)

                raw_row.append(column.format(raw_value))

            raw_data.append(raw_row)

        return raw_data

    def _make_title_row(self):
        return list([column.title for column in self._columns])

    def _calculate_column_widths(self, raw_data):
        column_widths = [-1] * len(raw_data[0])

        for row in raw_data:

            for column, cell in enumerate(row):
                # import ipdb; ipdb.set_trace()
                if len(cell) > column_widths[column]:
                    column_widths[column] = len(cell)

        return column_widths

    def _print(self, raw_data, column_widths, output):
        if len(raw_data) == 1:
            print('No data', file=output)
            return

        column_mask = []

        for column in range(0, len(raw_data[0])):
            column_mask += ["{{:{}}}".format(column_widths[column])]

        header_printed = False

        for row in raw_data:
            column = 0

            line = []

            for cell in row:
                line += [column_mask[column].format(cell)]

                column += 1

            formatted_line = "| {} |".format(" | ".join(line))

            print(formatted_line, file=output)

            if not header_printed:
                # TODO Improve
                print(" -{}-".format("-" * (len(formatted_line) - 4)), file=output)
                header_printed = True


class Column(object):

    def __init__(self, title, getter, formatter=lambda value: str(value)):
        self.title = title
        self._getter = getter
        self._formatter = formatter

    def get_value(self, row, data):
        return self._getter(row, data)

    def format(self, value):
        return self._formatter(value) if value is not None else ''
