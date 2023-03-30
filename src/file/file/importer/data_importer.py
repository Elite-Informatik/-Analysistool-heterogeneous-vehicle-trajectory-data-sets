from abc import ABC
from abc import abstractmethod

from src.data_transfer.record import DataRecord

STANDARD_SEP: str = ","


class DataImporter(ABC):
    """
    Abstract class representing a DataImporter.
    """


    def yield_import_data(self, path: str, sep: str = STANDARD_SEP) -> DataRecord:
        """
        Imports a file as Data from the given path.

        :param sep: standard separator
        :param path: path to the file to import
        :return: the imported data
        """
        pass

    @abstractmethod
    def import_data(self, path: str, sep: str = STANDARD_SEP) -> DataRecord:
        """
        Imports a file as Data from the given path.

        :param sep: standard separator
        :param path: path to the file to import
        :return: the imported data
        """
        pass

    @abstractmethod
    def fits_file_format(self, name: str) -> bool:
        """
        Check if the file _name fits the format of the importer

        :param name: file _name
        :return: True if the file format is supported, False otherwise
        """
        pass

    @property
    def file_format(self) -> str:
        """
        Returns a regex that can identify a file in the right format

        :return: a regex
        """
        raise NotImplemented("Not implemented!")
