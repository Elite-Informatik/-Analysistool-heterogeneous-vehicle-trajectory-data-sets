from typing import Optional
from uuid import UUID

from src.controller.execution_handling.filter_manager.filter_manager import IFilterGetter
from src.controller.execution_handling.filter_manager.filter_manager import IFilterManager
from src.controller.input_handling.commands.undoable import Undoable
from src.data_transfer.record import FilterGroupRecord


class ChangeFilterGroupCommand(Undoable):
    """
    represents a command to change a filter group
    """

    def __init__(self, group_id: UUID, new_group: FilterGroupRecord,
                 filter_manager: IFilterManager, filter_getter: IFilterGetter):
        """
        creates a new ChangeFilterGroupCommand
        :param group_id:       the id of the filter group to change
        :param new_group:      the new filter group parameters
        :param filter_manager: the filter manager
        """
        super().__init__()
        self._group_id = group_id
        self._new_group = new_group
        self._filter_manager = filter_manager
        self._filter_getter = filter_getter
        self._old_group: Optional[FilterGroupRecord] = None

    def undo(self):
        """
        undoes itself: resets the filter group parameters to the old ones
        """
        if self._old_group is not None:
            self._filter_manager.change_filter_group(self._group_id, self._old_group)

    def execute(self):
        """
        changes the filter group
        """
        self._old_group = self._filter_getter.get_filter_group_record(self._group_id)
        if self._old_group is not None:
            self._was_successful = self._filter_manager.change_filter_group(self._group_id, self._new_group)
