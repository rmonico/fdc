class TablePrinter(object):

    def __init__(self, fields, result_set):
        self._fields = fields
        self._result_set = result_set

    def print(self):
        self._load_and_format_data()

        self._calculate_column_widths()

        self._print()

    def _load_and_format_data(self):
        self._data = [[field['name'] for field in self._fields]]

        for row in self._result_set:
            formatted_row = ()

            for cell in self._get_cells(row):
                formatted_row += (self._format_cell(cell),)

            self._data += [formatted_row]

    def _get_cells(self, row):
        cells = []

        for field in self._fields:
            cells.append(getattr(row, field['name']))

        return cells

    @staticmethod
    def _format_cell(cell):
        return str(cell)

    def _calculate_column_widths(self):
        self._column_widths = [-1] * len(self._data[0])

        for row in self._data:

            for column, cell in enumerate(row):
                if len(cell) > self._column_widths[column]:
                    self._column_widths[column] = len(cell)

    def _print(self):
        if len(self._data) == 1:
            print('No data')
            return

        column_mask = []

        for column in range(0, len(self._data[0])):
            column_mask += ["{{:{}}}".format(self._column_widths[column])]

        header_printed = False

        for row in self._data:
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
