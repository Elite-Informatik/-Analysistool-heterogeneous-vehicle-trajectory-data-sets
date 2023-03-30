"""
filter_structure.py contains FilterStructure class.
"""
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from uuid import UUID

from src.data_transfer.content import FilterHandlerNames
from src.data_transfer.content.error import ErrorMessage
from src.data_transfer.content.logical_operator import LogicalOperator
from src.data_transfer.exception import InvalidUUID
from src.data_transfer.record import FilterGroupRecord
from src.data_transfer.record import FilterRecord
from src.model.error_handler import ErrorHandler
from src.model.filter_structure.filter_factory import FilterFactory
from src.model.filter_structure.filter_handler import FilterHandler
from src.model.filter_structure.ifilter_structure import IFilterStructure
from src.model.filter_structure.point_filter_visitor import PointFilterVisitor
from src.model.filter_structure.trajectory_filter_visitor import TrajectoryFilterVisitor
from src.model.polygon_structure.ipolygon_structure import IPolygonStructure


class FilterStructure(IFilterStructure, ErrorHandler):
    """
    Represents the filter facade of the model, which forms the interface of the filter structure to the
    controller. It reason is to check if
    """
    STANDART_ROOT_GROUP_NAME = "root group "

    def __init__(self, polygon_structure: IPolygonStructure):
        super().__init__()
        self._factory = FilterFactory(polygon_structure)
        handlers = [FilterHandlerNames.POINT_FILTER_HANDLER, FilterHandlerNames.TRAJECTORY_FILTER_HANDLER]
        self._filter_handlers: Dict[str, FilterHandler] = {}

        for handler in handlers:
            root_group = self._factory.create_group(
                FilterGroupRecord(
                    _name=self.STANDART_ROOT_GROUP_NAME + handler.value,
                    _structure_name=handler.value,
                    _enabled=True,
                    _negated=False,
                    _filter_records=(),
                    _operator=LogicalOperator.AND.name
                )
            )
            filter_handler = FilterHandler(root_group, handler.value)
            self._filter_handlers[handler.value] = filter_handler

        self._added_filter_components: List[Tuple[UUID, str]] = list()
        self._deleted_filter_components: List[Tuple[UUID, str]] = list()

    def _get_filter_handler_by_uuid(self, filter_component: UUID) -> Optional[FilterHandler]:
        for filter_handler in self._filter_handlers.values():
            if filter_handler.get_filter(filter_component):
                return filter_handler
            if filter_handler.get_filter_group(filter_component):
                return filter_handler

        return None

    def get_filter(self, filter_id: UUID) -> Optional[FilterRecord]:
        """
        gets the record of the filter with the given id
        :param filter_id:  the id of the filter
        :return:    the filter record
        """
        filter_handler = self._get_filter_handler_by_uuid(filter_id)
        if filter_handler is None:
            raise InvalidUUID("This filter does not exist!")

        found_filter = filter_handler.get_filter(filter_id)
        return found_filter.to_record(filter_handler.name)

    def get_filter_group(self, filter_group_id: UUID) -> Optional[FilterGroupRecord]:
        """
        gets the record of the filter group with the given id
        :param filter_group_id:  the id of the filter group
        :return:    the filter group record
        """
        filter_handler = self._get_filter_handler_by_uuid(filter_group_id)
        if filter_handler is None:
            raise InvalidUUID("This group does not exist!")

        found_filter_group = filter_handler.get_filter_group(filter_group_id)
        if found_filter_group is None:
            raise InvalidUUID("This group does not exist!")

        return found_filter_group.to_record(filter_handler.name)

    def get_point_sql_request(self) -> str:
        """
        gets the sql request of the filter and filter groups of the point filter handler
        :return: the sql request
        """
        visitor = PointFilterVisitor()
        self._filter_handlers['point filters'].accept_visitor(visitor)
        return visitor.get_sql_request()

    def get_trajectory_sql_request(self) -> str:
        """
        gets the sql request of the filter and filter groups of the trajectory filter handler
        :return: the sql request
        """
        visitor = TrajectoryFilterVisitor()
        self._filter_handlers['trajectory filters'].accept_visitor(visitor)
        return visitor.get_sql_request()

    def get_filter_types(self) -> List[str]:
        """
        gets all possible filter types
        :return: the filter types
        """
        return self._factory.possible_filter_types

    def get_standard_filter(self, filter_type: str) -> FilterRecord:
        """
        gets the record of a filter with standard values
        :param filter_type:    the filter type of the standard filter
        :return:        the standard filter record
        """
        return self._factory.create_standard_filter(filter_type) \
            .to_record(FilterHandlerNames.STANDART_FILTER_HANDLER_NAME.value)

    def get_standard_group(self) -> FilterGroupRecord:
        """
        gets the record of a filter group with standard values
        :return: the standard filter group record
        """
        return self._factory.create_standard_group().to_record(FilterHandlerNames.STANDART_FILTER_HANDLER_NAME.value)

    def move_filter_to_group(self, filter_id: UUID, group: UUID) -> bool:
        """
        moves the filter with the given filter id to the group with the given group id
        :param filter_id:  the id of the filter to move
        :param group:   the id of the group
        :return:        whether moving was successful
        """
        filter_handler = self._get_filter_handler_by_uuid(filter_id)
        # check if Filter exists
        if filter_handler is None:
            self.throw_error(ErrorMessage.FILTER_NOT_EXISTING)
            return False

        filter_to_move = filter_handler.get_filter(filter_id)
        # double check if Filter exists, this code should never be called
        if filter_id is None:
            self.throw_error(ErrorMessage.FILTER_NOT_EXISTING)
            raise RuntimeError("This code should never be called.")

        group_for_move = self.get_filter_group(group)
        # Checks if Group exists
        if group_for_move is None:
            self.throw_error(ErrorMessage.FILTER_GROUP_NOT_EXISTING)
            return False

        filter_handler.delete(filter_id)
        filter_handler.add(filter_to_move, group)
        return True

    def is_polygon_in_use(self, polygon_id: UUID) -> bool:
        """
        checks whether the polygon with the given id is used in one of the filter
        :param polygon_id:  the id of the polygon
        :return:    whether the polygon is used
        """
        for filter_handler in self._filter_handlers.values():
            if filter_handler.is_polygon_in_use(polygon_id):
                return True
        return False

    def add_filter(self, parent_id: UUID, parameters: FilterRecord) -> Optional[UUID]:
        """
        creates a new filter of the specified parameters and adds it to the filter structure.
        Does nothing and returns None if parent_id is invalid.
        :param parent_id:   the id of the group which the new filter should be added
        :param parameters:  the parameters of the new filter
        :return:            the id of the new filter
        """
        if parent_id is None or parameters is None:
            return None
        new_filter = self._factory.create_filter(parameters)
        filter_handler = self._filter_handlers[parameters.structure_name]

        if filter_handler is None:
            self.throw_error(ErrorMessage.INVALID_NAME)
            return None

        if not filter_handler.add(new_filter, parent_id):
            self.throw_error(ErrorMessage.FILTER_NOT_ADDED)
            return None

        if not new_filter.change(parameters):
            self.throw_error(ErrorMessage.FILTER_NOT_ADDED)
            return None

        self._added_filter_components.append(
            (new_filter.get_id(),
             filter_handler.name)
        )
        return new_filter.get_id()

    def add_filter_group(self, parent_id: UUID, parameters: FilterGroupRecord) -> Optional[UUID]:
        """
        creates a new filter group of the specified parameters and adds it to the filter structure
        :param parent_id:   the id of the group which the new filter group should be added
        :param parameters:  the parameters of the new filter group
        :return:            the id of the new filter group
        """
        new_group = self._factory.create_group(parameters)
        filter_handler = self._get_filter_handler_by_uuid(parent_id)

        if filter_handler is None:
            self.throw_error(ErrorMessage.NO_ABOVE_FILTER_GROUP)
            return None

        if not filter_handler.add(new_group, parent_id):
            self.throw_error(ErrorMessage.NO_ABOVE_FILTER_GROUP)
            return None

        new_group.change(parameters, list(), list())
        self._added_filter_components.append(
            (new_group.get_id(),
             filter_handler.name))
        return new_group.get_id()

    def undo_add(self) -> Optional[UUID]:
        """
        undoes the last addition of a filter component and deletes this filter component without saving it
        :return: the id of the delelted component
        """
        if len(self._added_filter_components) == 0:
            self.throw_error(ErrorMessage.NO_ADDABLE_COMPONENT)
            return None

        handler_tuple = self._added_filter_components.pop()
        filter_handler = self._filter_handlers[handler_tuple[1]]
        filter_handler.undo_add(handler_tuple[0])
        return handler_tuple[0]

    def delete_filter_component(self, filter_component_id: UUID) -> Optional[UUID]:
        """
        deletes the filter component with the given id
        :param filter_component_id:  the id
        :return: the parent id of the deleted component
        """
        filter_handler = self._get_filter_handler_by_uuid(filter_component_id)

        if filter_handler is None:
            self.throw_error(ErrorMessage.FILTER_NOT_DELETED)
            return None

        handler_tuple = (filter_component_id, filter_handler.name)
        if handler_tuple not in self._added_filter_components:
            self.throw_error(ErrorMessage.FILTER_NOT_DELETED)
            return None

        self._added_filter_components.remove(handler_tuple)
        self._deleted_filter_components.append(handler_tuple)
        parent_id = filter_handler.delete(filter_component_id)

        if parent_id is None:
            self.throw_error(ErrorMessage.FILTER_NOT_DELETED)
            return None

        return parent_id

    def reconstruct(self) -> Optional[UUID]:
        """
        reconstructs the last deleted filter component
        :return: the id of the reconstructed component
        """
        if len(self._deleted_filter_components) == 0:
            self.throw_error(ErrorMessage.RECONSTRUCTION_NOT_POSSIBLE)
            return None

        filter_handler = self._filter_handlers[self._deleted_filter_components.pop()[1]]
        filter_component_id = filter_handler.reconstruct()
        handler_tuple = (filter_component_id, filter_handler.name)
        self._added_filter_components.append(handler_tuple)
        return filter_component_id

    def change_filter(self, filter_id: UUID, parameters: FilterRecord) -> bool:
        """
        overwrites the attributes of the filter with the given id with the given parameters
        :param filter_id: the id of the filter to change
        :param parameters: the parameters
        """
        filter_handler = self._get_filter_handler_by_uuid(filter_id)
        if filter_handler is None:
            self.throw_error(ErrorMessage.FILTER_NOT_EXISTING)
            return False

        filter_to_change = filter_handler.get_filter(filter_id)
        if filter_to_change is None:
            self.throw_error(ErrorMessage.FILTER_NOT_EXISTING)
            return False

        return filter_to_change.change(parameters)

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
        filter_handler = self._get_filter_handler_by_uuid(filter_group_id)
        if filter_handler is None:
            self.throw_error(ErrorMessage.FILTER_GROUP_NOT_EXISTING)
            return False

        group_to_change = filter_handler.get_filter_group(filter_group_id)

        if group_to_change is None:
            self.throw_error(ErrorMessage.FILTER_GROUP_NOT_EXISTING)
            return False

        return group_to_change.change(parameters, filters, groups)

    def get_point_filter_root_id(self) -> UUID:
        """
        gets the root id of the point filter structure.
        :return: the root id of the root filter group.
        """
        return self._filter_handlers['point filters'].get_root_id()

    def get_trajectory_filter_root_id(self) -> UUID:
        """
        gets the root id of the trajectory filter structure.
        :return: the root id of the root filter group.
        """
        return self._filter_handlers['trajectory filters'].get_root_id()
