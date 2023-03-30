from enum import Enum


class FilterHandlerNames(Enum):
    """
    holds all names of the filter handlers
    """

    POINT_FILTER_HANDLER = 'point filters'
    TRAJECTORY_FILTER_HANDLER = 'trajectory filters'
    STANDART_FILTER_HANDLER_NAME = ''
