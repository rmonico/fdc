class TablePrinter(object):

    def __init__(self, columns):
        self._columns = columns

    def print(self, data):
        self._load_and_format_data(data)

        self._calculate_column_widths()

        self._print()

    def _load_and_format_data(self, _data):
        title_row = list()

        for column in self._columns:
            title_row.append(column.title)

        self._raw_data = [title_row]

        for row in _data:
            data = []
            for column in self._columns:
                value = column.get_value(row, _data)

                data.append(column.format(value))

            self._raw_data += [data]

    def _calculate_column_widths(self):
        self._column_widths = [-1] * len(self._raw_data[0])

        for row in self._raw_data:

            for column, cell in enumerate(row):
                # import ipdb; ipdb.set_trace()
                if len(cell) > self._column_widths[column]:
                    self._column_widths[column] = len(cell)

    def _print(self):
        if len(self._raw_data) == 1:
            print('No data')
            return

        column_mask = []

        for column in range(0, len(self._raw_data[0])):
            column_mask += ["{{:{}}}".format(self._column_widths[column])]

        header_printed = False

        for row in self._raw_data:
            column = 0

            line = []

            for cell in row:
                line += [column_mask[column].format(cell)]

                column += 1

            formatted_line = "| {} |".format(" | ".join(line))

            print(formatted_line)

            if not header_printed:
                # TODO Improve
                print(" -{}-".format("-" * (len(formatted_line) - 4)))
                header_printed = True


class Column(object):

    def __init__(self, title, getter, formatter=lambda value: str(value)):
        self.title = title
        self._getter = getter
        self._formatter = formatter

    def get_value(self, row, data):
        return self._getter(row, data)

    def format(self, value):
        return self._formatter(value) if value else ''


class AttrGetter(object):
    def __init__(self, attr_name, default=None):
        self._attr_name = attr_name
        self._default = default

    def get(self, row, data):
        return getattr(row, self._attr_name, self._default)

def format_currency(value):
    return '{:.2f}'.format(value) if value else ''

def attr_column(attribute, formatter=lambda v: str(v)):
    return Column(attribute.capitalize(), AttrGetter(attribute).get, formatter)
