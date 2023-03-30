"""
filter_factory.py contains FilterFactory class.
"""
import uuid
from typing import List

from src.data_transfer.content.logical_operator import LogicalOperator
from src.data_transfer.name_generator import NameGenerator
from src.data_transfer.record.filter_group_record import FilterGroupRecord
from src.data_transfer.record.filter_record import FilterRecord
from src.model.filter_structure.composite.filter_group import FilterGroup
from src.model.filter_structure.composite.filters.abstract_filter import Filter
from src.model.filter_structure.composite.filters.discrete_filter import DiscreteFilter
from src.model.filter_structure.composite.filters.interval_filter import IntervalFilter
from src.model.filter_structure.composite.filters.polygon_filter import PolygonFilter
from src.model.polygon_structure.ipolygon_structure import IPolygonStructure


class FilterFactory:
    """
    represents a factory to create filters and filters groups
    """
    FILTER_TYPES = {'discrete filter': DiscreteFilter,
                    'interval filter': IntervalFilter,
                    'polygon filter': PolygonFilter}
    _STANDARD_NAME = 'filter'

    def __init__(self, polygon_structure: IPolygonStructure):
        self._polygon_structure = polygon_structure

    @property
    def possible_filter_types(self) -> List[str]:
        """
        Getter for the possibel filter types of the factory
        :return: possible filter types of the factory
        """
        return list(self.FILTER_TYPES.keys())

    def create_filter(self, filter_record: FilterRecord) -> Filter:
        """
        creates a filters of the specified type and the given parameters
        :param filter_record:   the parameters of the filters
        :return:                the new filters
        """
        filter_type = self.FILTER_TYPES[filter_record.type]
        filter_object = filter_type(uuid.uuid4(), filter_record.name)
        if filter_object.needs_polygons is True:
            filter_object.set_polygon_structure(self._polygon_structure)
        filter_object.change(filter_record)
        return filter_object

    @staticmethod
    def create_group(group: FilterGroupRecord) -> FilterGroup:
        """
        creates a new filters group of the given parameters
        :param group:   the parameters
        :return:        the new filters group
        """
        return FilterGroup(LogicalOperator[group.operator], uuid.uuid1(), group.name)

    def create_standard_filter(self, filter_type: str) -> Filter:
        """
        creates a new filters with standard values
        :param filter_type:    the type of the filters to create
        :return:        the new standard filters
        """
        filter_constructor = self.FILTER_TYPES[filter_type]
        filter_object = filter_constructor(uuid.uuid4(), NameGenerator.get_name(self._STANDARD_NAME))

        if filter_object.needs_polygons is True:
            filter_object.set_polygon_structure(self._polygon_structure)
            filter_object.set_polygons([])
        return filter_object

    def create_standard_group(self) -> FilterGroup:
        """
        creates a new filters group with standard values
        :return:    the new standard filters group
        """
        return FilterGroup(LogicalOperator.AND, uuid.uuid1(), self._STANDARD_NAME)
