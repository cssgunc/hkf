import csv
import typing


class CSVHandler:
    def __init__(self, name: str):
        self.path = f"./{name}.csv"
        with open(self.path, "w", newline='') as file:
            pass

    def add_rows(self, rows: list[list[str]]):
        with open(self.path, "a", newline='') as file:
            writer = csv.writer(file, dialect='excel')
            writer.writerows(rows)

    def add_row(self, row: list[str]):
        self.add_rows([row])