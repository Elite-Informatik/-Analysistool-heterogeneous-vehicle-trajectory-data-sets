from typing import Optional
from uuid import UUID

from src.controller.execution_handling.polygon_manager import IPolygonManager
from src.controller.input_handling.commands.undoable import Undoable
from src.data_transfer.record import PolygonRecord


class DeletePolygonCommand(Undoable):
    """
    represents a command to delete polygons
    """

    def __init__(self, polygon_id: UUID, polygon_manager: IPolygonManager):
        """
        creates a new DeletePolygonCommand
        :param polygon_id:      the id of the polygon to delete
        :param polygon_manager: the polygon manager
        """
        super().__init__()
        self._polygon_id = polygon_id
        self._polygon_manager = polygon_manager
        self._deleted_polygon: Optional[PolygonRecord] = None

    def undo(self):
        """
        undoes itself: adds a new polygon with the parameters of the deleted polygon
        """
        self._polygon_manager.undo_deletion()

    def execute(self):
        """
        deletes the polygon
        """
        self._was_successful = self._polygon_manager.delete_polygon(self._polygon_id)
