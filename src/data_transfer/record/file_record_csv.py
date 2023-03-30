import os

from pandas import DataFrame

from src.data_transfer.record import FileRecord


class FileRecordCsv(FileRecord):
    """
    represents a csv file
    """

    def __init__(self, data_frame: DataFrame, name: str):
        self._file_name: str = name
        self._data_frame: DataFrame = data_frame

    def save(self, path: str):
        self._data_frame.to_csv(os.path.join(path, self._file_name + ".csv"))
