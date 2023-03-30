from abc import abstractmethod
from typing import Callable
from typing import List
from typing import Optional

from src.data_transfer.record import DataRecord
from src.data_transfer.record import FileRecord
from src.model.error_handler import ErrorHandler


class FileFacade(ErrorHandler):
    """
    This interface is responsible for all file operations on the operating system. It also takes
    over the converting process of the application specific datasets.
    """

    @abstractmethod
    def set_standard_paths(self, analysis_standart_path: str, dictionary_standart_path: str) -> bool:
        """
        Setter for the standart paths of the FileFacade.
        :param analysis_standart_path: analysis standart path from the src directory
        :param dictionary_standart_path: dictionary standart path from the src directory
        :return: if paths exist
        """
        pass

    @abstractmethod
    def export_data_file(self, path: str, data: DataRecord, file_format: str) -> bool:
        """
        This method exports a given data_record to a given path

        :param path: THe path to export to
        :param data: The data to export
        :param file_format: The format of the datatype

        :return: None
        """

        pass

    @abstractmethod
    def import_data_files(self, chucked_path: str, inaccuracies: List[str]):
        """
        These methods imports given data files
        @param chucked_path: The path to import from
        @param inaccuracies: The list of inaccuracies
        :return: The information of the data files converted to DatRecords (if possible)
        """

        pass

    @abstractmethod
    def open_session(self, allways_imported, file_format) -> None:
        """
        This method opens a session
        :param allways_imported: if the file should be imported
        :param file_format: the file format
        """
        pass

    def close_session(self):
        """
        This method closes a session
        """
        pass

    @abstractmethod
    def export_file(self, path: str, file: FileRecord) -> bool:
        """
        These methods export a generic file to the given path

        :param path: the path given in a string
        :param file: The given file in a file record

        :return: whether export was successful
        """

        pass

    @abstractmethod
    def export_dictionary_to_standard_path(self, name: str, dictionary: dict) -> bool:
        """
        This method exports a dictionary.
        The program uses a standard path to exports its own long-lasting data.

        :param name: The _name of the dictionary
        :param dictionary:  itself

        :return: bool
        """

        pass

    @abstractmethod
    def import_dictionary_from_standard_path(self, name: str) -> dict:
        """
        This method imports a dictionary from a given _name.
        The program uses a standard path to exports its own long-lasting data.

        :param name: The _name of the dictionary to import

        :return: The found dictionary
        """

        pass

    @abstractmethod
    def get_analysis_types_from_standard_path(self) -> List[Callable[[], object]]:
        """
        This method imports all analyses from the standard program path

        :return: The List of callable analyses
        """

        pass

    @abstractmethod
    def import_new_analysis_to_standard_path(self, from_path: str) -> bool:
        """
        This method imports an analysis from another path to the standard program path

        :param from_path: The origin path of an analysis

        :return: Whether the import was sucessful
        """

        pass

    @abstractmethod
    def exportable_file_formats(self) -> List[str]:
        """
        Gets all exportable file formats

        :return: list of all file formats in a string format
        """
        pass

    @property
    def convertabele_file_formats(self) -> List[str]:
        """
        all convertable file formats
        """
        raise NotImplemented
