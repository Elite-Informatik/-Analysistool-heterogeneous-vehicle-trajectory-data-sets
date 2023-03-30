from typing import Optional
from uuid import UUID

from src.controller.execution_handling.filter_manager.filter_manager import IFilterGetter
from src.controller.execution_handling.filter_manager.filter_manager import IFilterManager
from src.controller.input_handling.commands.undoable import Undoable
from src.data_transfer.record import FilterRecord


class ChangeFilterCommand(Undoable):
    """
    represents a command to change a filter
    """

    def __init__(self, filter_id: UUID, new_filter: FilterRecord,
                 filter_manager: IFilterManager, filter_getter: IFilterGetter):
        """
        creates a new ChangeFilterCommand
        :param filter_id:       the id of the filter to change
        :param new_filter:      the new filter parameters
        :param filter_manager:  the filter manager
        """
        super().__init__()
        self._filter_id = filter_id
        self._new_filter = new_filter
        self._filter_manager = filter_manager
        self._filter_getter = filter_getter
        self._old_filter: Optional[FilterRecord] = None

    def undo(self):
        """
        undoes itself: resets the filter parameters to the old ones
        """
        if self._old_filter is not None:
            self._filter_manager.change_filter(self._filter_id, self._old_filter)

    def execute(self):
        """
        changes the filter
        """
        self._old_filter = self._filter_getter.get_filter_record(self._filter_id)
        if self._old_filter is not None:
            self._was_successful = self._filter_manager.change_filter(self._filter_id, self._new_filter)
