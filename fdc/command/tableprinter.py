#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class TablePrinter(object):

    def __init__(self, fields, result_set):
        self._fields = fields
        self._result_set = result_set

    def print(self):
        self._load_and_format_data()

        self._calculate_column_widths()

        self._print()

    def _load_and_format_data(self):
        self._data = []

        self._data += [self._fields]

        for row in self._result_set:
            formatted_row = ()

            for cell in row:
                formatted_row += (self._format_cell(cell), )

            self._data += [formatted_row]

    def _format_cell(self, cell):
        return str(cell)

    def _calculate_column_widths(self):
        self._column_widths = [-1] * len(self._data[0])

        for row in self._data:

            column = 0
            for cell in row:
                if len(cell) > self._column_widths[column]:
                    self._column_widths[column] = len(cell)

                column += 1

    def _print(self):
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
