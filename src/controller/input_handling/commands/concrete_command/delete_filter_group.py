from typing import Optional
from uuid import UUID

from src.controller.execution_handling.filter_manager.filter_manager import IFilterManager
from src.controller.input_handling.commands.undoable import Undoable


class DeleteFilterGroupCommand(Undoable):
    """
    represents a command to delete a filter group
    """

    def __init__(self, group_id: UUID, filter_manager: IFilterManager):
        """
        creates a new DeleteFilterGroupCommand
        :param group_id:        the filter group to delete
        :param filter_manager:  the filter manager
        """
        super().__init__()
        self._group_id = group_id
        self._filter_manager = filter_manager
        self._parent_id: Optional[UUID] = None

    def undo(self):
        """
        undoes itself: adds the deleted filter group back to the filter structure
        """
        if self._parent_id is not None:
            self._filter_manager.reconstruct_filter_group(self._parent_id)

    def execute(self):
        """
        deletes the filter group
        """
        self._parent_id = self._filter_manager.delete(self._group_id)
        self._was_successful = self._parent_id is not None
