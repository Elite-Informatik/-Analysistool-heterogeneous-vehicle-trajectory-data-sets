from datetime import datetime
from datetime import time
from typing import List

from src.data_transfer.selection.option import Option
from src.data_transfer.selection.option_type import OptionType


class TimeIntervalOption(Option):
    """
    Implements an Option that is used to select Time Intervals. Since the
    input and out put of the Selections should always be a datatype that can
    be used for sql queries and a time as a string is not comparable it is the job of this
    class is to solve this Problem. The input and output will always be a time in the String Format.
    Intern the class converts the String to a time object to proof if the date interval is valid.
    """

    TIME_FORMAT = "%H:%M:%S"
    SQL_FORMAT = "'{data}'"

    def __init__(self, start: str = None, end: str = None):
        """
        Creates a new TimeIntervalOption.
        If not interval Borders are given, the Interval accepts all times.
        :param start: string of format HH:MM:SS (TIME FORMAT) that indicates the start of the interval
        :param end: string of format HH:MM:SS (TIME FORMAT) that indicates the end of the interval
        """
        super().__init__(option_type=OptionType.TIME_INTERVAL_OPTION)
        if start is None:
            self._start = time.min
        else:
            self._start = datetime.strptime(start, self.TIME_FORMAT).time()
        if end is None:
            self._end = time.max
        else:
            self._end = datetime.strptime(end, self.TIME_FORMAT).time()

    def is_valid(self, option) -> bool:
        """
        Poofs if a given Interval is valid.
        :param option: a tuple where option[0] and option[1] are both time strings of format TIME_FORMAT
        :return True if the Interval is valid otherwise false
        """
        try:
            start_interval = datetime.strptime(option[0], self.TIME_FORMAT).time()
        except ValueError:
            return False
        try:
            end_interval = datetime.strptime(option[1], self.TIME_FORMAT).time()
        except ValueError:
            return False
        return self._start <= start_interval <= end_interval <= self._end

    def get_option(self) -> []:
        """
        Returns a tuple where the first value is the start of the interval and the second Value is the end of the
        interval. Both strings are formatted with the HH:MM:SS (TIME FORMAT) format
        """
        return [time.strftime(self._start, self.TIME_FORMAT), time.strftime(self._end, self.TIME_FORMAT)]

    def sql_format(self) -> List[str]:
        """
        returns the format of the date for sql queries
        """
        return self.SQL_FORMAT
