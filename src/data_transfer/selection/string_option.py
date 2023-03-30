import re

from src.data_transfer.selection.option import Option
from src.data_transfer.selection.option_type import OptionType


class StringOption(Option):
    """
    Class representing a string option for a selection
    """
    _valid_string: str

    def __init__(self, valid_string: str):
        """
        Initialize a StringOption instance with a regular expression describing valid strings

        :param valid_string: A regular expression describing the valid strings for this option
        """
        super().__init__(OptionType.STRING_OPTION)
        self._valid_string = valid_string

    def is_valid(self, option: str) -> bool:
        """
        Check if the given option matches the regular expression describing valid strings

        :param option: The value to check if it matches the regular expression
        :return: True if the option matches the regular expression, False otherwise
        """
        return re.fullmatch(self._valid_string, option) is not None

    def get_option(self) -> []:
        """
        Get the regular expression describing valid strings as a list of characters

        :return: A list containing the characters of the regular expression
        """
        return list(self._valid_string)
