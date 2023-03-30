from enum import Enum


class SettingContext(Enum):
    """
    contains all setting contexts of filter (group) records
    """

    POLYGON = "Polygon"
    INTERVAL = "Interval"
    TIME_INTERVAL = "Time Interval"
    NUMBER_INTERVAL = "Number Interval"
    DATE_INTERVAL = "Date Interval"
    DISCRETE = "Discrete"
    LOGICAL_OPERATOR = "Operator"
    COLUMN = "Column"
