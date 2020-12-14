from unittest import TestCase
from commons.tableprinter import Column, TablePrinter
import io


class TablePrinterTests(TestCase):

    def test_should_print_single_column(self):
        columns = list()
        columns.append(Column('ID', lambda row, data: row[0]))
        columns.append(Column('Value', lambda row, data: row[1]))

        printer = TablePrinter(columns)

        data = list()
        data.append((1, 'First line'))
        data.append((2, 'Second line'))

        output_file = io.StringIO()

        printer.print(data, output_file)

        output = output_file.getvalue().splitlines()

        self.assertRegex(output[0], '^\| ID +\| Value +\|$')
        self.assertRegex(output[1], '^ -+$')
        self.assertRegex(output[2], '^\| 1 +\| First line +\|$')
        self.assertRegex(output[3], '^\| 2 +\| Second line +\|$')
        self.assertEqual(len(output), 4)

    def test_should_format_data(self):
        columns = list()
        columns.append(Column('ID', lambda row, data: row[0]))
        columns.append(Column('Even?', lambda row, data: row[0] % 2 == 0, lambda value: 'Yes' if value else 'No'))

        printer = TablePrinter(columns)

        data = [ (value, ) for value in range(1, 5) ]

        output_file = io.StringIO()

        printer.print(data, output_file)

        output = output_file.getvalue().splitlines()

        self.assertRegex(output[0], '^\| ID +\| Even\? +\|$')
        self.assertRegex(output[1], '^ -+$')
        self.assertRegex(output[2], '^\| 1 +\| No +\|$')
        self.assertRegex(output[3], '^\| 2 +\| Yes +\|$')
        self.assertRegex(output[4], '^\| 3 +\| No +\|$')
        self.assertRegex(output[5], '^\| 4 +\| Yes +\|$')
        self.assertEqual(len(output), 6)
