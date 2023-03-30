"""
filter_handler.py contains FilterHandler Class.
"""

from typing import List
from typing import Optional
from typing import Tuple
from uuid import UUID

from src.model.filter_structure.composite.filter_component import FilterComponent
from src.model.filter_structure.composite.filter_group import FilterGroup
from src.model.filter_structure.composite.filters.abstract_filter import Filter
from src.model.filter_structure.filter_visitor import IVisitor


class FilterHandler:
    """
    represents the filter structure which holds all filter and filter groups in form of the composite pattern
    """

    def __init__(self, root: FilterGroup, name: str):
        """
        creates a new FilterStructure
        :param root: the root group (entry point to the composite)
        """
        assert isinstance(root, FilterGroup)

        self._name = name
        self._root_group = root
        self._deleted_components: List[Tuple[FilterComponent, UUID]] = list()

    @property
    def name(self) -> str:
        """
        Name of the Filter handler.
        :return: the _name.
        """
        return self._name

    def add(self, component: FilterComponent, group: UUID) -> bool:
        """
        adds a new filter component to the group with the given group id
        :param component: the new filter component to add
        :param group:     the id of the group which the component should be added
        :return:          whether the component could be successfully added
        """
        return self._root_group.add(component, group)

    def undo_add(self, component_id: UUID) -> bool:
        """
        undoes the last addition of a filter component and deletes this filter component without saving it
        :param component_id:    the id of the component to delete
        :return:                if the deletion was successful
        """
        return self._root_group.delete(component_id) is not None

    def reconstruct(self) -> Optional[UUID]:
        """
        reconstructs the last deleted filter component
        """
        if len(self._deleted_components) == 0:
            return None

        reconstructed_component = self._deleted_components.pop()
        self.add(reconstructed_component[0], reconstructed_component[1])
        return reconstructed_component[0].get_id()

    def is_deleted_component_id(self, component_id: UUID) -> bool:
        """
        Function returns if filterhandler is responsible for deleted component by uuid.
        :param component_id: the uuid of the deleted component.
        :return: If component id is a deleted component of this filter handler.
        """
        if len(self._deleted_components) == 0:
            return False
        return component_id == self._deleted_components[0][0].get_id()

    def delete(self, component_id: UUID) -> Optional[UUID]:
        """
        deletes the filter component with the specified id and saves the deleted component
        :param component_id: the id of the component to delete
        :return:   the parent id of the deleted component (if existent)
        """
        if component_id == self._root_group.get_id():
            return None

        deleted_component = self._root_group.get(component_id)
        if deleted_component is None:
            return None

        parent_id = self._root_group.delete(component_id)

        self._deleted_components.append((deleted_component, parent_id))
        return parent_id

    def accept_visitor(self, v: IVisitor) -> None:
        """
        accepts a visitor and passes it to the root group
        :param v:   the visitor
        """
        self._root_group.accept_visitor(v)

    def get_filter(self, uuid: UUID) -> Optional[Filter]:
        """
        gets the filter with the given id
        :param uuid:  the id
        :return:    the filter with the given id
        """
        return self._root_group.get_filter(uuid)

    def get_filter_group(self, uuid: UUID) -> Optional[FilterGroup]:
        """
        gets the filter group with the given id
        :param uuid:  the id
        :return:    the filter group with the given id
        """
        return self._root_group.get_filter_group(uuid)

    def is_polygon_in_use(self, uuid: UUID) -> bool:
        """
        checks whether the polygon of the given id is used in one of the filters
        :param uuid:  the id of the polygon
        :return:    whether the polygon is used by a filter
        """
        return self._root_group.is_polygon_in_use(uuid)

    def get_root_id(self) -> UUID:
        """
        gets the id of the root group
        :return: the id of the root group
        """
        return self._root_group.get_id()
