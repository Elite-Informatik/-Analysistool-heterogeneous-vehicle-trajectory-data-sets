from abc import abstractmethod
from typing import Generic
from typing import TypeVar

from src.data_transfer.selection.option_type import OptionType

T = TypeVar("T")


class Option(Generic[T]):
    """
    this abstract class represents an option
    """

    _option_type: OptionType

    def __init__(self, option_type: OptionType):
        self._optionType = option_type

    @abstractmethod
    def is_valid(self, option) -> bool:
        """
        whether the selected option is valid
        :param option:  the selected value
        :return         whether the selected option is valid
        """
        raise NotImplementedError

    @abstractmethod
    def get_option(self) -> []:
        """
        the selected values
        """
        raise NotImplementedError

    def get_option_type(self) -> OptionType:
        """
        gets the type of this option
        """
        return self._optionType

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.get_option_type().__eq__(other.get_option_type()) and (self.get_option() == other.get_option())

    def __str__(self):
        return f"{self._optionType}\n" \
               f"\toptions: {self.get_option()}"
