"""
filter_group.py contains FilterGroup class.
"""

from typing import List
from typing import Optional
from uuid import UUID

from src.data_transfer.content.logical_operator import LogicalOperator
from src.data_transfer.record.filter_group_record import FilterGroupRecord
from src.model.filter_structure.composite.filter_component import FilterComponent
from src.model.filter_structure.composite.filters.abstract_filter import Filter
from src.model.filter_structure.filter_visitor import IVisitor


class FilterGroup(FilterComponent):
    """
    represents a filters group and therefore the composite in the Composite Pattern
    """

    def __init__(self, logical_operator: LogicalOperator, filter_id: UUID, name: str):
        super().__init__(filter_id=filter_id, name=name)
        self._logical_operator: LogicalOperator = logical_operator
        self._filters: List[FilterComponent] = list()

    def get_filter(self, filter_id: UUID) -> Optional[Filter]:
        """
        gets the filters with the given id if contained in this group
        :param filter_id:  the filters id
        :return:    the filters with the given id
        """
        for filter_component in self._filters:
            return_filter = filter_component.get_filter(filter_id)
            if return_filter is not None:
                return return_filter

        return None

    def get_filter_group(self, filter_group_id: UUID) -> Optional['FilterGroup']:
        """
        gets the filters group with the given id if contained in this group
        :param filter_group_id:  the filters group id
        :return:    the filters group with the given id
        """
        if self.get_id() == filter_group_id:
            return self

        for filter_component in self._filters:
            return_group = filter_component.get_filter_group(filter_group_id)
            if return_group is not None:
                return return_group

        return None

    def get(self, component_id: UUID) -> Optional[FilterComponent]:
        """
        gets the filter component with the given id if contained in this group
        :param component_id:  the id of the filter component
        :return:              the filter component with the given id
        """
        if self.get_id() == component_id:
            return self

        for filter_component in self._filters:
            if filter_component.get(component_id) is not None:
                return filter_component.get(component_id)

        return None

    def delete(self, filter_component_id: UUID) -> Optional[UUID]:
        """
        deletes the filters component with the given id if contained in this group
        :param filter_component_id:  the id of the filters component
        :return:    the parent id of the deleted component
        """
        for filter_component in self._filters:
            if filter_component.get_id() == filter_component_id:
                self._filters.remove(filter_component)
                return self.get_id()

        for filter_component in self._filters:
            parent_id = filter_component.delete(filter_component_id)
            if parent_id is not None:
                return parent_id

        return None

    def accept_visitor(self, v: IVisitor) -> None:
        """
        accepts the given visitor and passes it to the children
        :param v:   the visitor
        """
        if not self._enabled:
            return
        v.start_group(self._logical_operator, self._negated)
        for filter_component in self._filters:
            filter_component.accept_visitor(v)
        v.leave_group()

    def add(self, component: FilterComponent, group_id: UUID) -> bool:
        """
        adds the given filters component to the group if the given group_id matches its own,
        otherwise pass the method to the children
        :param component:   the new component
        :param group_id:    the id of the group which the commponent should be added
        :return:
        """
        assert issubclass(component.__class__, FilterComponent)

        if group_id != self._id:
            for filter_component in self._filters:
                if filter_component.add(component, group_id):
                    return True
            return False
        else:
            self._filters.append(component)
            return True

    def is_polygon_in_use(self, polygon_id: UUID) -> bool:
        """
        checks whether the polygon of the given id is used in one of the children
        :param polygon_id:  the id of the polygon
        :return:    whether the polygon is used
        """
        for filter_component in self._filters:
            if filter_component.is_polygon_in_use(polygon_id):
                return True
        return False

    def change(self, group: FilterGroupRecord, filters: List[UUID], filter_goups: List[UUID]):
        """
        changes the attributes of itself and its children
        @param group: the new attributes
        @param filter_goups: the filter groups which were changed
        @param filters: the filters which were changed
        """
        self._logical_operator = LogicalOperator[group.operator]
        self._name = group.name
        self._negated = group.negated
        self.change_enabled(group.enabled, filters, filter_goups)
        if not (self._id in filter_goups):
            filter_goups.append(self._id)

    def to_record(self, structure_name: str) -> FilterGroupRecord:
        """
        converts itself to a record
        :return:    the filters group record of itself
        """
        filter_records: List[UUID] = list()
        for filter_component in self._filters:
            filter_records.append(filter_component.get_id())

        return FilterGroupRecord(
            _name=self._name,
            _structure_name=structure_name,
            _enabled=self._enabled,
            _negated=self._negated,
            _filter_records=tuple(filter_records),
            _operator=self._logical_operator.name
        )

    def change_enabled(self, enabled: bool, filters: List[UUID], filter_groups: List[UUID]):
        """
        changes the enabled attribute of itself and its children
        @param enabled:  the new value
        @param filter_groups:  the filter groups which were changed
        @param filters: the filters which were changed
        """
        if self._enabled == enabled:
            return
        super().change_enabled(enabled, filters, filter_groups)
        filter_groups.append(self.get_id())
        for filter_component in self._filters:
            filter_component.change_enabled(enabled, filters, filter_groups)
