from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Optional
from uuid import UUID

from src.controller.execution_handling.abstract_manager import AbstractManager
from src.controller.execution_handling.filter_manager.filterer import IFilterGetter
from src.controller.facade_consumer.data_facade_consumer import DataFacadeConsumer
from src.controller.facade_consumer.filter_facade_consumer import FilterFacadeConsumer
from src.controller.facade_consumer.setting_facade_consumer import SettingFacadeConsumer
from src.controller.output_handling.event import FilterAdded
from src.controller.output_handling.event import FilterChanged
from src.controller.output_handling.event import FilterComponentDeleted
from src.controller.output_handling.event import FilterGroupAdded
from src.controller.output_handling.event import FilterGroupChanged
from src.controller.output_handling.event import FilterMovedToGroup
from src.controller.output_handling.event import RefreshTrajectoryData
from src.data_transfer.content import type_check
from src.data_transfer.record import FilterGroupRecord
from src.data_transfer.record import FilterRecord


class IFilterManager(ABC):
    """
    This interface is used to change the filters structure in the model layer controlled.
    """

    @abstractmethod
    def reconstruct_filter(self, parent: UUID) -> bool:
        """
        This method reconstructs the last deleted filter component
        :param parent: The parent uuid
        :return: The list of resulting events
        """

        pass

    @abstractmethod
    def reconstruct_filter_group(self, parent: UUID) -> bool:
        """
        This method reconstructs the last deleted filter group
        :param parent: The parent uuid
        :return: The list of resulting events
        """

        pass

    @abstractmethod
    def add_filter(self, parent: UUID, parameter: FilterRecord) -> bool:
        """
        This method adds a given filters in the model layer
        :param parent: The parent uuid
        :param parameter: The specific parameters in a FIlterRecord
        :return: whether adding the filter was successful
        """

        pass

    @abstractmethod
    def add_filter_group(self, parent: UUID, parameter: FilterGroupRecord) -> bool:
        """
        This method adds a given filters group in the model layer
        :param parent: The parent uuid
        :param parameter: The specific parameters in a FilterRecord
        :return: whether adding the filter group was successful
        """

        pass

    @abstractmethod
    def delete(self, uuid: UUID) -> UUID:
        """
        This method deletes a filters in the model layer
        :param uuid: The uuid of the filters to delete
        :return: id of the deleted filter
        """

        pass

    @abstractmethod
    def undo_add(self):
        """
        undoes the addition of the last filter component and deletes it without saving it
        :return:                the list of resulting events
        """

    @abstractmethod
    def move_filter_to_group(self, filter_uuid: UUID, group_uuid: UUID) -> bool:
        """
        This method moves a given filters to a specific group in the model layer

        :param filter_uuid: the filters to move
        :param group_uuid: the group the filters is moved to

        :return: whether moving the filter was successful
        """

        pass

    @abstractmethod
    def change_filter(self, uuid: UUID, parameters: FilterRecord) -> bool:
        """
        This method changes the parameters of a given filters
        :param uuid: The uuid of the filters to change
        :param parameters: The updated parameters
        :return: whether changing the filter was successful
        """

        pass

    @abstractmethod
    def change_filter_group(self, uuid: UUID, parameters: FilterGroupRecord) -> bool:
        """
        This method changes the parameters of a given filters group
        :param uuid: The uuid of the filters to change
        :param parameters: The updated parameters
        :return: whether changing the filter group was successful
        """

        pass


class FilterManager(IFilterManager, AbstractManager,
                    IFilterGetter, FilterFacadeConsumer, DataFacadeConsumer,
                    SettingFacadeConsumer):
    """
    This class implements the InterfaceFilterManager. It uses the IFilterFacade, the SettingFacade and the
    DataFacade via the parental classes.
    """

    USE_FILTER: bool = True
    NEGATE_FILTER: bool = False

    @type_check(UUID, FilterRecord)
    def add_filter(self, parent_id: UUID, parameters: FilterRecord) -> bool:

        new_filter_id = self.filter_facade.add_filter(parent_id, parameters)

        if new_filter_id is None:
            self.handle_error([self.filter_facade])
            return False

        self.update_data_filter()
        self.events.extend([FilterAdded(new_filter_id, parent_id), RefreshTrajectoryData()])
        self.handle_event()
        return True

    @type_check(UUID, FilterGroupRecord)
    def add_filter_group(self, parent_id: UUID, parameters: FilterGroupRecord) -> bool:
        new_group_id = self.filter_facade.add_filter_group(parent_id, parameters)

        if new_group_id is None:
            self.handle_error([self.filter_facade])
            return False

        self.update_data_filter()
        self.events.extend([FilterGroupAdded(new_group_id, parent_id), RefreshTrajectoryData()])
        self.handle_event()
        return True

    def undo_add(self) -> bool:

        filter_component_id = self.filter_facade.undo_add()
        if filter_component_id is None:
            self.handle_error([self.filter_facade])
            return False

        self.update_data_filter()
        self.events.extend([FilterComponentDeleted(filter_component_id), RefreshTrajectoryData()])
        self.handle_event()
        return True

    @type_check(UUID)
    def delete(self, component_id: UUID) -> Optional[UUID]:

        parent_id = self.filter_facade.delete(component_id)

        if parent_id is None:
            self.handle_error([self.filter_facade])
            return None

        self.update_data_filter()
        self.events.extend([FilterComponentDeleted(component_id), RefreshTrajectoryData()])
        self.handle_event()
        return parent_id

    def _reconstruct(self) -> Optional[UUID]:
        filter_component_id = self.filter_facade.reconstruct()
        if filter_component_id is None:
            self.handle_error([self.filter_facade])
            return None

        self.update_data_filter()
        return filter_component_id

    @type_check(UUID)
    def reconstruct_filter(self, parent_id: UUID) -> bool:

        filter_component_id = self._reconstruct()
        if filter_component_id is None:
            return False

        self.events.extend([FilterAdded(filter_component_id, parent_id), RefreshTrajectoryData()])
        self.handle_event()
        return True

    @type_check(UUID)
    def reconstruct_filter_group(self, parent_id: UUID) -> bool:

        filter_component_id = self._reconstruct()
        if filter_component_id is None:
            return False

        self.events.extend([FilterGroupAdded(filter_component_id, parent_id), RefreshTrajectoryData()])
        self.handle_event()
        return True

    @type_check(UUID, FilterGroupRecord)
    def move_filter_to_group(self, filter_uuid: UUID, group_uuid: UUID) -> bool:

        if not self.filter_facade.move_filter_to_group(filter_uuid, group_uuid):
            self.handle_error([self.filter_facade])
            return False

        self.update_data_filter()
        self.events.extend([FilterMovedToGroup(filter_uuid, group_uuid), RefreshTrajectoryData()])
        self.handle_event()
        return True

    @type_check(UUID, FilterRecord)
    def change_filter(self, filter_id: UUID, parameters: FilterRecord) -> bool:

        if not self.filter_facade.change_filter(filter_id, parameters):
            self.handle_error([self.filter_facade])
            return False

        self.update_data_filter()
        self.events.extend([FilterChanged(filter_id), RefreshTrajectoryData()])
        self.handle_event()
        return True

    @type_check(UUID, FilterGroupRecord)
    def change_filter_group(self, group_id: UUID, parameters: FilterGroupRecord) -> bool:
        filter_ids = list()
        filter_group_ids = list()
        self.filter_facade.change_filter_group(group_id, parameters, filter_ids, filter_group_ids)

        if len(filter_group_ids) == 0:
            self.handle_error([self.filter_facade])
            return False

        self.update_data_filter()
        for filter_id in filter_ids:
            self.events.append(FilterChanged(filter_id))

        for filter_group_id in filter_group_ids:
            self.events.append(FilterGroupChanged(filter_group_id))

        for filter_id in filter_ids:
            self.events.append(FilterChanged(filter_id))
        self.events.append(RefreshTrajectoryData())
        self.handle_event()
        return True

    def update_data_filter(self) -> bool:

        sql_string = self.filter_facade.get_point_sql_request()
        if sql_string is not None:
            self.data_facade.set_point_filter(sql_string, self.USE_FILTER, self.NEGATE_FILTER)
        else:
            self.data_facade.set_point_filter("", False, self.NEGATE_FILTER)

        sql_string = self.filter_facade.get_trajectory_sql_request()
        if sql_string is not None:
            self.data_facade.set_trajectory_filter(sql_string, self.USE_FILTER)
        else:
            self.data_facade.set_trajectory_filter("", False)

        return True

    @type_check(UUID)
    def get_filter_record(self, filter_id: UUID) -> Optional[FilterRecord]:
        filter_record: FilterRecord = self.filter_facade.get_filter(filter_id)
        if filter_record is None:
            self.handle_error([self.filter_facade])
            return None
        return filter_record

    @type_check(UUID)
    def get_filter_group_record(self, group_id: UUID) -> Optional[FilterGroupRecord]:
        filter_group: FilterGroupRecord = self.filter_facade.get_filter_group(group_id)
        if filter_group is None:
            self.handle_error([self.filter_facade])
            return None
        return filter_group

    @type_check(str)
    def get_filter_selections(self, filter_type: str) -> Optional[FilterRecord]:
        filter_record: FilterRecord = self.filter_facade.get_standard_filter(filter_type)
        if filter_record is None:
            self.handle_error([self.filter_facade])
            return None
        return filter_record

    def get_filter_group_selection(self) -> Optional[FilterGroupRecord]:

        filter_group: FilterGroupRecord = self.filter_facade.get_standard_group()
        if filter_group is None:
            self.handle_error([self.filter_facade])
            return None
        return filter_group

    def get_filter_types(self) -> List[str]:

        types: list = self.filter_facade.get_filter_types()
        if len(types) == 0:
            self.handle_error([self.filter_facade])
            return []

        return types

    def get_point_filters_root(self) -> Optional[UUID]:
        """
        gets the uuid of the root group of the point filters
        :return: the uuid of the root group of the point filters
        """
        uuid: UUID = self.filter_facade.get_point_filters_root()
        if uuid is None:
            self.handle_error([self.filter_facade])
            return None
        return uuid

    def get_trajectory_filters_root(self) -> Optional[UUID]:
        """
        gets th uuid of the root group of the trajectory filters
        :return: the root group of the trajectory filters
        """
        uuid: UUID = self.filter_facade.get_trajectory_filters_root()
        if uuid is None:
            self.handle_error([self.filter_facade])
            return None
        return uuid
