from src.data_transfer.selection.option import Option
from src.data_transfer.selection.option_type import OptionType


class IntervalValueOption(Option):
    """
    Class representing an interval option for a selection
    """

    def __init__(self, start, end):
        """
        Initialize an IntervalOption instance with a start and an end value

        :param start: The start value of the interval
        :param end: The end value of the interval
        """
        super().__init__(OptionType.INTERVAL_OPTION)
        self._start = start
        self._end = end

    def is_valid(self, option) -> bool:
        """
        Check if the given option is within the interval defined by the start and end values

        :param option: The value to check if it is within the interval
        :return: True if the option is within the interval, False otherwise
        """
        return self._start <= option <= self._end

    def get_option(self) -> []:
        """
        Get the start and end values of the interval as a list

        :return: A list containing the start and end values of the interval
        """
        return [self._start, self._end]

    def sql_format(self) -> str:
        """
        returns the format of the date
        """
        return "{data}"
