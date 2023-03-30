import os

import pandas as pd

from src.data_transfer.record import DataRecord
from src.file.file.importer.data_importer import DataImporter

STANDARD_SEP: str = ","


class CSVImporter(DataImporter):
    """
    Class representing a CSVImporter.
    """

    def fits_file_format(self, name: str) -> bool:
        return name.endswith(".csv")

    def import_data(self, path: str, sep: str = STANDARD_SEP) -> DataRecord:
        file_name = os.path.splitext(os.path.basename(path))
        dataframe = pd.read_csv(path, delimiter=sep)
        return DataRecord(file_name[0], dataframe.columns, dataframe)

    def yield_import_data(self, path: str, sep: str = STANDARD_SEP) -> DataRecord:
        file_name = os.path.splitext(os.path.basename(path))
        for dataframe in pd.read_csv(path, delimiter=sep, chunksize=100000):
            yield DataRecord(file_name[0], dataframe.columns, dataframe)

    @property
    def file_format(self) -> str:
        return r'^.*\.csv$'
