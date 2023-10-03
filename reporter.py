from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo


class Reporter:
    def __init__(self, headers):
        self.workbook = Workbook()
        self.headers = headers
        self.workbook.active.append(headers)
        self.end_column = chr(ord('A') + len(headers) - 1)


    def write_data_to_table(self, data):
        for row in data:
            self.workbook.active.append(row)

        tab = Table(displayName="Report", ref=f"A1:{self.end_column}{str(len(data)+1)}")
        style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,
                               showLastColumn=False, showRowStripes=True, showColumnStripes=True)
        tab.tableStyleInfo = style
        self.workbook.active.add_table(tab)

    def write_data(self, filename):
        self.workbook.save(filename)
