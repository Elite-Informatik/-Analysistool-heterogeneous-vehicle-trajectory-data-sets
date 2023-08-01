import os
from io import StringIO

import textract

import pandas as pd
from typing import TextIO

from src.data_transfer.record import DataRecord
from src.file.file.importer.data_importer import DataImporter

STANDARD_SEP: str = ","


class DocImporter(DataImporter):
    """
    Imports a doc file as Data. The doc file must contain data in a csv format.
    Most of the lines have to be in the csv format.
    """

    def yield_import_data(self, path: str, sep: str = STANDARD_SEP) -> DataRecord:
        """
        Imports each doc file from the given path and yields the imported data after each file.
        """
        for file in os.listdir(path):
            if self.fits_file_format(file):
                data = self.import_data(os.path.join(path, file), sep)
                # checks if the data is empty
                # todo: remove
                print("current_file: ", file)
                if data.data.empty:
                    continue
                print("\tnot empty")
                yield data

    def import_data(self, path: str, sep: str = STANDARD_SEP) -> DataRecord:
        """
        Imports the doc file as Data from the given path.

        :param sep: standard separator
        :param path: path to the file to import
        :return: the imported data
        """
        file_name = os.path.splitext(os.path.basename(path))
        text = textract.process(path)

        lines = text.splitlines()
        average_line_length = sum(len(line.split(b',')) for line in lines) / len(lines)
        items_per_line = round(average_line_length)
        csv_lines = []
        for line in lines:
            if len(line.split(b',')) == items_per_line:
                csv_lines.append(line.decode("utf-8"))

        if len(csv_lines) == 0:
            return DataRecord(file_name[0], [], pd.DataFrame())

        csv_file = StringIO("\n".join(csv_lines))

        dataframe = pd.read_csv(csv_file, delimiter=sep)

        if dataframe.empty:
            return DataRecord(file_name[0], (), pd.DataFrame())

        return DataRecord(file_name[0], dataframe.columns, dataframe)
    def fits_file_format(self, name: str) -> bool:
        """
        Check if the file _name fits the format of the importer

        :param name: file _name
        :return: True if the file format is supported, False otherwise
        """
        return name.endswith(".doc") or "." not in name

    @property
    def file_format(self) -> str:
        """
        Returns a regex that can identify a file in the right format

        :return: a regex
        """
        return r'^.*\[.doc]?$'
