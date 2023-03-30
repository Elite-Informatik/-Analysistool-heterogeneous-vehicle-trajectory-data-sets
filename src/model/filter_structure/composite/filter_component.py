"""
filter_component.py File contains FilterComponent class.
"""
from typing import List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.model.filter_structure.filter_visitor import IVisitor
    from src.model.filter_structure.composite.filters.abstract_filter import Filter
    from src.model.filter_structure.composite.filter_group import FilterGroup

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID


class FilterComponent(ABC):
    """
    Filter Component is super class for filter composite.
    """

    def __init__(self, negated: bool = False, enabled: bool = True, name: str = None, filter_id: UUID = None):
        self._id: UUID = filter_id
        self._negated: bool = negated
        self._enabled: bool = enabled
        self._name: str = name

    def add(self, component: 'FilterComponent', group_id: UUID) -> bool:
        """
        adds a new filters component to the group with the given group id
        :param group_id: the id of the group which the component should be added
        :param component: the new filters component to add
        :return:          whether the component could be successfully added
        """
        return False

    def delete(self, filter_component_id: UUID) -> Optional[UUID]:
        """
        deletes the filters component with the specified id
        :param filter_component_id: the id of the component to delete
        :return:   the parent id of the deleted component if the deletion was successful
        """
        return None

    @abstractmethod
    def get_filter(self, filter_id: UUID) -> Optional['Filter']:
        """
        gets the filters with the given id
        :param filter_id:  the id
        :return:    the filters with the given id
        """
        pass

    def get_filter_group(self, filter_group_id: UUID) -> Optional['FilterGroup']:
        """
        gets the filters group with the given id
        :param filter_group_id:  the id
        :return:    the filters group with the given id
        """
        return None

    def get(self, component_id: UUID) -> Optional['FilterComponent']:
        """
        gets the filter component with the given id
        :param component_id: the id of the filter component 
        :return:          the filter component with the given id
        """
        if self._id == component_id:
            return self
        return None

    def is_polygon_in_use(self, polygon_id: UUID) -> bool:
        """
        Checks for a polygon if it is in use inside the filter component.
        :param polygon_id: the uuid of the polygon
        :return: if the filter component contains the polygon
        """
        return False

    def get_id(self) -> UUID:
        """
        gets the id of the filters component
        :return: the id
        """
        return self._id

    @abstractmethod
    def accept_visitor(self, v: 'IVisitor') -> None:
        """
        accepts a filter visitor.
        :param v: the visitor to accept.
        """
        pass

    def change_enabled(self, enabled: bool, filters: List[UUID], filter_groups: List[UUID]):
        """
        changes the enabled state of the filter component
        @param enabled:   the new enabled state
        @param filter_groups:  the filter groups which are changed
        @param filters: the filters which are changed
        """
        self._enabled = enabled
