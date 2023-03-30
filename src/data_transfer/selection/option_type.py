from enum import Enum


class OptionType(Enum):
    """
    holds all available option types
    """

    DISCRETE_OPTION = "Selection"
    INTERVAL_OPTION = "Interval"
    STRING_OPTION = "Name"
    BOOL_OPTION = "True/False"
    DATE_INTERVAL_OPTION = "Date Interval"
    NUMBER_INTERVAL_OPTION = "Number Interval"
    TIME_INTERVAL_OPTION = "Time Interval"
