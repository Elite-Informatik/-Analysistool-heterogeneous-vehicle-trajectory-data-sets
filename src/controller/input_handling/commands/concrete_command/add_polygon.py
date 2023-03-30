from typing import Optional
from uuid import UUID

from src.controller.execution_handling.polygon_manager import IPolygonManager
from src.controller.input_handling.commands.undoable import Undoable
from src.data_transfer.record import PolygonRecord


class AddPolygonCommand(Undoable):
    """
    represents a command to add a new polygon to the polygon structure
    """

    def __init__(self, polygon: PolygonRecord, manager: IPolygonManager):
        """
        creates a new AddPolygonCommand
        :param polygon:         the new polygon
        :param manager:         the polygon manager
        """
        super().__init__()
        self._polygon = polygon
        self._manager = manager
        self._polygon_id: Optional[UUID] = None

    def undo(self):
        """
        undoes itself: deletes the added polygon
        """
        self._manager.undo_addition()

    def execute(self):
        """
        adds the new polygon to the polygon structure
        """
        self._was_successful = (self._manager.add_polygon(self._polygon) is not None)
