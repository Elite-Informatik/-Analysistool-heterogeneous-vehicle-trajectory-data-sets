from typing import Optional
from uuid import UUID

from src.controller.execution_handling.filter_manager.filter_manager import IFilterManager
from src.controller.input_handling.commands.undoable import Undoable


class DeleteFilterCommand(Undoable):
    """
    represents a command to delete a filter
    """

    def __init__(self, filter_id: UUID, filter_manager: IFilterManager):
        """
        creates a new DeleteFilterCommand
        :param filter_id:       the filter to delete
        :param filter_manager:  the filter manager
        """
        super().__init__()
        self._filter_id = filter_id
        self._filter_manager = filter_manager
        self._parent_id: Optional[UUID] = None

    def undo(self):
        """
        undoes itself: adds the deleted filter back to the filter structure
        """
        if self._parent_id is not None:
            self._filter_manager.reconstruct_filter(self._parent_id)

    def execute(self):
        """
        deletes the filter
        """
        self._parent_id = self._filter_manager.delete(self._filter_id)
        self._was_successful = self._parent_id is not None
