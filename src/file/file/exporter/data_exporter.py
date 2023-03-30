from abc import ABC
from abc import abstractmethod

from pandas import DataFrame


class DataExporter(ABC):
    """
    Abstract class representing a DataExporter.
    """

    @abstractmethod
    def export_data(self, path: str, data: DataFrame):
        """
        Exports data in a specific file format to the given path.

        :param path: path to export the data to
        :param data: data to export
        """
        pass

    @abstractmethod
    def get_file_format(self) -> str:
        """
        Returns the file format that can be exported by the class.

        :return: file format _name
        """
        pass
