import datetime
from datetime import datetime as _datetime
from typing import List

from src.data_transfer.selection.option import Option
from src.data_transfer.selection.option_type import OptionType


class DateIntervalOption(Option):
    """
    Implements an Option that is used to select Date Intervals. Since the
    input and out put of the Selections should always be a datatype that can
    be used for sql queries and a date as a string is not comparable it it the job of this
    class is to solve this Problem. The input and output will always be a date in the String Format.
    Intern the class converts the String to a datetime object to proof if the date interval is valid.
    """

    DATE_FORMAT = "%Y-%m-%d"
    SQL_FORMAT = "'{data}'"

    def __init__(self, start: str = "", end: str = ""):
        """
        Creates a new DateIntervalOption. If no start and end date is set the
        date range will be the largest date range possible in the datetime module.
        :param start: date as a string of Format YYYY-MM-DD
        :param end: date as a string of Format YYYY-MM-DD
        """
        super().__init__(option_type=OptionType.DATE_INTERVAL_OPTION)
        if start == "":
            self._start = datetime.date(1000, 1, 1)
        else:
            self._start = _datetime.strptime(start, self.DATE_FORMAT).date()
        if end == "":
            self._end = datetime.date(datetime.MAXYEAR, 1, 1)
        else:
            self._end = _datetime.strptime(end, self.DATE_FORMAT).date()

    def is_valid(self, option) -> bool:
        """
        Proofs if the given interval is valid
        :param option: a Tuple (start, end) where start and end are both date strings of Format YYYY-MM-DD
        """
        try:
            start_interval = _datetime.strptime(option[0], self.DATE_FORMAT).date()
        except ValueError:
            return False
        try:
            end_interval = _datetime.strptime(option[1], self.DATE_FORMAT).date()
        except ValueError:
            return False
        return self._start <= start_interval <= end_interval <= self._end

    def get_option(self) -> List[str]:
        """
        returns borders of the interval
        return: a Tuple (start, end) of the interval size where start and end are date strings of Format YYYY-MM-DD
        """
        return [_datetime.strftime(self._start, self.DATE_FORMAT), _datetime.strftime(self._end, self.DATE_FORMAT)]

    def sql_format(self) -> str:
        """
        returns the format of the date for sql queries
        """
        return self.SQL_FORMAT
