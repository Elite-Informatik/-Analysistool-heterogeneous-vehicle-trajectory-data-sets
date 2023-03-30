from abc import ABC
from abc import abstractmethod

from src.data_transfer.record import FilterRecord


class FilterCreator(ABC):
    """
    This is an interface that needs to be implemented by all dialogs that create and modify concrete filters.
    """

    @abstractmethod
    def is_valid(self) -> bool:
        """
        This method is used to proof if the input of the user to the dialog is valid after the dialog has been
        closed.
        """
        pass

    @abstractmethod
    def get_new_filter(self) -> FilterRecord:
        """
        Returns a Filter Record that contains a filter based on the user input. This method should only be called
        when the is_valid method returns True.
        """
        pass
