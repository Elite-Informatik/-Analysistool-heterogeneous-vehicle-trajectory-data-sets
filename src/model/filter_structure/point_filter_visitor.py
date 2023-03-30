"""
point_filter_visitor.py contains PointFilterVisiotr class.
"""

from typing import TYPE_CHECKING

from src.data_transfer.content.logical_operator import LogicalOperator
from src.model.filter_structure.filter_visitor import IVisitor

if TYPE_CHECKING:
    from src.model.filter_structure.composite.filters.interval_filter import IntervalFilter
    from src.model.filter_structure.composite.filters.polygon_filter import PolygonFilter
    from src.model.filter_structure.composite.filters.discrete_filter import DiscreteFilter


class PointFilterVisitor(IVisitor):
    """
    Point Filter Visitor Class visits filters for point sql-string.
    """

    def visit_interval_filter(self, interval_filter: 'IntervalFilter') -> None:
        """
        Visits an interval filter. Adds the fitler string to itself.
        :param interval_filter: the filter to be addet to the filter string.
        """
        self._current_filters.append(self._create_interval_filter_str(
            column=interval_filter.column.value,
            start=interval_filter.start,
            end=interval_filter.end)
        )

    def visit_polygon_filter(self, polygon_filter: 'PolygonFilter') -> None:
        """
        visits a Polygon filter
        :param polygon_filter: the polygon filter to visit
        """
        self.start_group(LogicalOperator.AND, False)
        for polygon_filter in self._create_polygons_filter_strs(polygon_filter.polygons):
            self._current_filters.append(polygon_filter)
        self.leave_group()

    def visit_discrete_filter(self, discrete_filter: 'DiscreteFilter') -> None:
        """

        :param discrete_filter:
        """
        self._current_filters.append(self._create_discrete_filter_str(
            column=discrete_filter.column.value,
            values=discrete_filter.selection
        ))
