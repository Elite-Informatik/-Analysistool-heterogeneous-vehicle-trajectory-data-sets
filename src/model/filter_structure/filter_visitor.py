"""
filter_visitor.py contains IVisitor class.
"""
from typing import List
from typing import TYPE_CHECKING

from src.data_transfer.content import Column

if TYPE_CHECKING:
    from src.model.filter_structure.composite.filters.interval_filter import IntervalFilter
    from src.model.filter_structure.composite.filters.polygon_filter import PolygonFilter
    from src.model.filter_structure.composite.filters.discrete_filter import DiscreteFilter

from abc import ABC, abstractmethod

from src.data_transfer.content.logical_operator import LogicalOperator
from src.data_transfer.record import PolygonRecord


class IVisitor(ABC):
    """
    This interface represents an interface to iterate through a filters structure, according to the Visitor Pattern.
    """
    INTERVAL_FILTER = '({column} between {start} and {end})'
    POLYGON_FILTER = 'ST_Contains(ST_MakePolygon(ST_GeomFromText(\'LINESTRING({positions})\')), ST_POINT(latitude, longitude))'
    DISCRETE_FILTER = '({column} in ({selection}))'
    KOMMA_SEPERATOR = ', '

    def __init__(self):
        self._groups: list[tuple[LogicalOperator, bool]] = []
        self._filters: list[list[str]] = []
        self._current_filters: list[str] = []

    @abstractmethod
    def visit_interval_filter(self, interval_filter: 'IntervalFilter') -> None:
        """
        visits a IntervalFilter
        :param interval_filter:  the interval filters to visit
        """
        pass

    @abstractmethod
    def visit_polygon_filter(self, polygon_filter: 'PolygonFilter') -> None:
        """
        visits a Polygon filter
        :param polygon_filter: the polygon filter to visit
        """
        pass

    @abstractmethod
    def visit_discrete_filter(self, discrete_filter: 'DiscreteFilter') -> None:
        """
        visits a DiscreteFilter
        :param discrete_filter:  the discrete filter to visit
        """
        pass

    def start_group(self, operator: 'LogicalOperator', negated: bool) -> None:
        """
        enters a group with the given operator
        :param operator: the logical operator of the visited group
        :param negated: whether the group is negated
        """
        self._filters.append(self._current_filters)
        self._current_filters = []
        self._groups.append((operator, negated))

    def leave_group(self) -> None:
        """
        leaves the current group
        """
        operator, negated = self._groups.pop()

        if len(self._current_filters) != 0:
            new_filter = operator.join_requests(self._current_filters)
            new_filter = self._negate_filter(new_filter, negated)

            self._current_filters = self._filters.pop()
            self._current_filters.append(new_filter)
        else:
            self._current_filters = self._filters.pop()

    def get_sql_request(self) -> str:
        """
        returns the sql-request, created while visiting the filters structure
        :return: the created sql-request
        """
        if len(self._current_filters) == 0:
            return ""
        return self._current_filters[0]

    def _create_polygons_filter_strs(self, polygons: List[PolygonRecord]) -> List[str]:
        polygon_filters = []
        for polygon in polygons:
            filter_str = self._create_polygon_filter_str(polygon)
            polygon_filters.append(filter_str)
        return polygon_filters

    def _create_polygon_filter_str(self, polygon) -> str:
        corners_strs = []
        for corner in polygon.corners:
            corners_strs.append(str(corner))
        corners_strs.append(str(polygon.corners[0]))
        positions = self.KOMMA_SEPERATOR.join(corners_strs)
        filter_str = self.POLYGON_FILTER.format(positions=positions)
        return filter_str

    def _create_interval_filter_str(self, column: str, start: int, end: int) -> str:
        return self.INTERVAL_FILTER.format(column=column, start=start, end=end)

    def _create_discrete_filter_str(self, column: str, values: List[str]) -> str:
        value_str = list()
        for value in values: # TODO: Remove this quick 'n dirty fix
            if value in Column.list():
                value_str.append(str(value))
            else:
                value_str.append("'" + str(value) + "'")
        return self.DISCRETE_FILTER.format(column=column, selection=self.KOMMA_SEPERATOR.join(value_str))

    def _negate_filter(self, filter_str: str, negated: bool) -> str:
        if not negated:
            return filter_str
        return f"NOT ({filter_str})"
