from abc import ABC
from abc import abstractmethod

from src.data_transfer.record import FilterGroupRecord


class FilterGroupCreator(ABC):
    """
    This is an interface that needs to be implemented by the FilterGroupDialogs
    """

    @abstractmethod
    def is_valid(self) -> bool:
        """
        proofs if the user input to the dialog was valid after the dialog has been closed.
        return: True if valid false otherwise
        """
        pass

    @abstractmethod
    def get_new_filter_group(self) -> FilterGroupRecord:
        """
        Takes the input form the user and creates a new FilterGroupRecord. This method should only be called
        when the is_valid method returned True.
        """
        pass
