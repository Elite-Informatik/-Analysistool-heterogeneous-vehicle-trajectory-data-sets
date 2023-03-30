"""
ifilter_structure.py contains IFilterStructure class.
"""

from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Optional
from uuid import UUID

from src.data_transfer.record import FilterGroupRecord
from src.data_transfer.record import FilterRecord


class IFilterStructure(ABC):
    """
    represents the filter facade of the model, which forms the interface of the filter structure to the
    controller
    """

    @abstractmethod
    def move_filter_to_group(self, filter_id: UUID, group: UUID) -> bool:
        """
        moves the filter with the given filter id to the group with the given group id
        :param filter_id:  the id of the filter to move
        :param group:   the id of the group
        :return:        whether moving was successful
        """
        pass

    @abstractmethod
    def get_filter(self, filter_id: UUID) -> Optional[FilterRecord]:
        """
        gets the record of the filter with the given id
        :param filter_id:  the id of the filter
        :return:    the filter record
        """
        pass

    @abstractmethod
    def get_filter_group(self, filter_group_id: UUID) -> Optional[FilterGroupRecord]:
        """
        gets the record of the filter group with the given id
        :param filter_group_id:  the id of the filter group
        :return:    the filter group record
        """
        pass

    @abstractmethod
    def get_point_sql_request(self) -> str:
        """
        gets the sql request of the filter and filter groups of the point filter handler
        :return: the sql request
        """
        pass

    @abstractmethod
    def get_trajectory_sql_request(self) -> str:
        """
        gets the sql request of the filter and filter groups of the trajectory filter handler
        :return: the sql request
        """
        pass

    @abstractmethod
    def get_filter_types(self) -> List[str]:
        """
        gets all possible filter types
        :return: the filter types
        """
        pass

    @abstractmethod
    def get_standard_filter(self, filter_type: str) -> FilterRecord:
        """
        gets the record of a filter with standard values
        :param filter_type:    the filter type of the standard filter
        :return:        the standard filter record
        """
        pass

    @abstractmethod
    def get_standard_group(self) -> FilterGroupRecord:
        """
        gets the record of a filter group with standard values
        :return: the standard filter group record
        """
        pass

    @abstractmethod
    def is_polygon_in_use(self, polygon_id: UUID) -> bool:
        """
        checks whether the polygon with the given id is used in one of the filter
        :param polygon_id:  the id of the polygon
        :return:    whether the polygon is used
        """
        pass

    @abstractmethod
    def add_filter(self, parent_id: UUID, parameters: FilterRecord) -> UUID:
        """
        creates a new filter of the specified parameters and adds it to the filter structure.
        Does nothing and returns None if parent_id is invalid.
        :param parent_id:   the id of the group which the new filter should be added
        :param parameters:  the parameters of the new filter
        :return:            the id of the new filter
        """
        pass

    @abstractmethod
    def add_filter_group(self, parent_id: UUID, parameters: FilterGroupRecord) -> Optional[UUID]:
        """
        creates a new filter group of the specified parameters and adds it to the filter structure
        :param parent_id:   the id of the group which the new filter group should be added
        :param parameters:  the parameters of the new filter group
        :return:            the id of the new filter group
        """
        pass

    @abstractmethod
    def undo_add(self) -> Optional[UUID]:
        """
        undoes the last addition of a filter component and deletes this filter component without saving it
        :return: the id of the delelted component
        """
        pass

    @abstractmethod
    def delete_filter_component(self, filter_component_id: UUID) -> Optional[UUID]:
        """
        deletes the filter component with the given id
        :param filter_component_id:  the id
        :return: the parent id of the deleted component
        """
        pass

    @abstractmethod
    def reconstruct(self) -> Optional[UUID]:
        """
        reconstructs the last deleted filter component
        :return: the id of the reconstructed component
        """
        pass

    @abstractmethod
    def change_filter(self, filter_id: UUID, parameters: FilterRecord) -> bool:
        """
        overwrites the attributes of the filter with the given id with the given parameters
        :param filter_id: the id of the filter to change
        :param parameters: the parameters
        """
        pass

    @abstractmethod
    def change_filter_group(self, filter_group_id: UUID, parameters: FilterGroupRecord, filters: List[UUID],
                            groups: List[UUID]):
        """
        overwrites the attributes of the filter gorup with the given id with the given parameters
        :param filter_group_id: the id of the filter group to change
        :param parameters:  the parameters
        :param filters: the ids of the filters which are changed
        :param groups: the ids of the filter groups which are changed
        :return: the ids of the filters which are changed
        """
        pass

    @abstractmethod
    def get_point_filter_root_id(self) -> UUID:
        """
        gets the root id of the point filter structure.
        :return: the root id of the root filter group.
        """
        pass

    @abstractmethod
    def get_trajectory_filter_root_id(self) -> UUID:
        """
        gets the root id of the trajectory filter structure.
        :return: the root id of the root filter group.
        """
        pass
