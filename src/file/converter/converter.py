from abc import ABC
from abc import abstractmethod
from typing import List

from src.data_transfer.record import DataRecord

STANDARD_SEP: str = ","


class Converter(ABC):
    """
    this abstract class converts a data object of a certain format into another dataformat
    """

    @abstractmethod
    def is_convertable(self, data: List[DataRecord]) -> bool:
        """
        This abstract method takes a list of DataRecord objects as an argument and returns a boolean indicating
        whether the data can be converted.

        :param data: List of DataRecord objects
        :return: Indicates whether the data can be converted
        """
        pass

    @abstractmethod
    def search_inaccuracies(self, data: List[DataRecord]) -> List[str]:
        """
        This abstract method takes a list of DataRecord objects as an argument and returns a list of strings
        indicating any inaccuracies found in the data.
        :param data: List of DataRecord objects
        :return: List of inaccuracies found in the data # todo define format of inaccuracies
        """
        pass

    def get_separator(self) -> str:
        """
        Returns the separator, which is used to separate the csv files
        """
        return STANDARD_SEP

    def open_session(self):
        """
        This method opens a session
        """
        pass

    def close_session(self):
        """
        This method closes a session
        """
        pass
