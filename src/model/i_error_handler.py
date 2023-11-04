from abc import ABC
from typing import List

from src.data_transfer.record import ErrorRecord


class IErrorHandler(ABC):
    """
    An interface for objects that can handle and return error messages.

    Any class that implements this interface is able to track and report error messages. The `get_errors()` method
    should be implemented to return a list of all errors encountered by the implementing object and all its
    underlying objects.
    """

    def __init__(self):
        """
        Constructor for IErrorHandler.
        """
        self.errors: List[ErrorRecord] = []

    def get_errors(self) -> List[ErrorRecord]:
        """
        Returns a list of all errors encountered by the implementing object and all its underlying objects.

        :return: A list of all errors encountered by the implementing object and all its underlying objects.
        """
        errors: List = self.errors.copy()
        self.errors.clear()
        return errors

    def error_occured(self) -> bool:
        """
        Returns whether an error has occurred.

        :return: Whether an error has occurred. True if it has, False otherwise.
        """
        return len(self.errors) > 0
