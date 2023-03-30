from uuid import UUID

from src.controller.execution_handling.filter_manager.filter_manager import IFilterManager
from src.controller.input_handling.commands.undoable import Undoable
from src.data_transfer.record import FilterGroupRecord


class AddFilterGroupCommand(Undoable):
    """
    represents a command to add a new filter group
    """

    def __init__(self,
                 new_filter_group: FilterGroupRecord,
                 parent: UUID,
                 filter_manager: IFilterManager):
        """
        creates a new AddFilterGroupCommand
        :param new_filter_group:    the new filter group to add
        :param parent:              the parent id to which the filter group should be added
        :param filter_manager:      the filter manager
        """
        super().__init__()
        self._new_filter_group = new_filter_group
        self._parent = parent
        self._filter_manager = filter_manager

    def undo(self):
        """
        undoes itself: deletes the added filter group
        """
        self._filter_manager.undo_add()

    def execute(self):
        """
        adds the new filter group to the filter structure
        """
        self._was_successful = self._filter_manager.add_filter_group(self._parent, self._new_filter_group)
