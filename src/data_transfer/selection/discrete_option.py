from typing import List

from src.data_transfer.selection.option import Option
from src.data_transfer.selection.option_type import OptionType


class DiscreteOption(Option):
    """
    represents an option with discrete values
    """

    _options: tuple

    def __init__(self, options: list):
        super().__init__(OptionType.DISCRETE_OPTION)
        self._options = tuple(options)

    def is_valid(self, option) -> bool:
        for self_option in self._options:
            if option == self_option:
                return True
        return False

    def get_option(self) -> List:
        return list(self._options)
