from enum import Enum


class FilterType(Enum):
    """
    represents all possible filters types
    """

    TRANSIT = "polygon filter"
    AREA = "polygon filter"
    DISCRETE = "discrete filter"
    INTERVAL = "interval filter"
