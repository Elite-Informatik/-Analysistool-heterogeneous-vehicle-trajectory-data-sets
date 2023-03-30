from typing import Optional
from uuid import UUID

from src.controller.execution_handling.filter_manager.filter_manager import IFilterManager
from src.controller.input_handling.commands.undoable import Undoable


class MoveFilterToGroupCommand(Undoable):
    """
    represents a command to move a filter into a filter group
    """

    def __init__(self, filter_uuid: UUID, group: UUID, filter_manager: IFilterManager):
        """
        creates a new MoveFilterToGroupCommand
        :param filter_uuid:          the filter to move
        :param group:           the group
        :param filter_manager:  the filter manager
        """
        super().__init__()
        self._filter = filter_uuid
        self._group = group
        self._filter_manager = filter_manager
        self._old_group: Optional[UUID] = None

    def undo(self):
        """
        undoes itself: moves the moved filter back into the old group
        """
        self._filter_manager.move_filter_to_group(self._filter, self._old_group)

    def execute(self):
        """
        moves the filter into the group
        """
        self._was_successful = self._filter_manager.move_filter_to_group(self._filter, self._group)
