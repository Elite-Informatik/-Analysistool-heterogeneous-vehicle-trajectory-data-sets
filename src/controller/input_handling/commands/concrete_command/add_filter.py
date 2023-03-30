from uuid import UUID

from src.controller.execution_handling.filter_manager.filter_manager import IFilterManager
from src.controller.input_handling.commands.undoable import Undoable
from src.data_transfer.record import FilterRecord


class AddFilterCommand(Undoable):
    """
    represents a command to add a new filter
    """

    def __init__(self, new_filter: FilterRecord, parent: UUID, filter_manager: IFilterManager):
        """
        creates a new AddFilterCommand
        :param new_filter:      the new filter to add
        :param parent:          the parent id to which the filter should be added
        :param filter_manager:  the filter manager
        """
        super().__init__()
        self._new_filter: FilterRecord = new_filter
        self._parent: UUID = parent
        self._filter_manager: IFilterManager = filter_manager

    def undo(self):
        """
        undoes itself: deletes the added filter
        """
        self._filter_manager.undo_add()

    def execute(self):
        """
        adds the new filter to the filter structure
        """
        self._was_successful = (self._filter_manager.add_filter(self._parent, self._new_filter) is not None)
