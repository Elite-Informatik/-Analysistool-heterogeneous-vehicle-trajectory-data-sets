import sys

from src.data_transfer.selection.option import Option
from src.data_transfer.selection.option_type import OptionType


class NumberIntervalOption(Option):
    """
    Represents a numeric interval option
    """

    SQL_FORMAT = "{data}"

    def __init__(self, start: float = None, end: float = None):
        super().__init__(OptionType.NUMBER_INTERVAL_OPTION)

        if start is None:
            self._start = -sys.float_info.max
        else:
            self._start = start
        if end is None:
            self._end = sys.float_info.max
        else:
            self._end = end

    def is_valid(self, option) -> bool:
        return self._start <= option[0] <= option[1] <= self._end

    def get_option(self) -> []:
        return [self._start, self._end]

    def sql_format(self) -> str:
        """
        returns the format of the date for sql queries
        """
        return self.SQL_FORMAT
