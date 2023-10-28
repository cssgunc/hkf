import csv
from io import StringIO

class CSVHandler:
    def __init__(self):
        self.line = StringIO()
        self.writer = csv.writer(self.line)

    def add_rows(self, rows: list[list[str]]):
        self.writer.writerows(rows)

    def add_row(self, row: list[str]):
        self.add_rows([row])