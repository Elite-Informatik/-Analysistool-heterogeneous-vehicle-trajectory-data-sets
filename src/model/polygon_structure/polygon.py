import re
import uuid
from typing import List
from typing import Optional
from uuid import UUID

from src.data_transfer.content.error import ErrorMessage
from src.data_transfer.exception import ExecutionFlowError
from src.data_transfer.record import PolygonRecord
from src.data_transfer.record import PositionRecord

INVALID_EXECUTION_MSG: str = "Error, invalid execution flow"


class Polygon:
    """
    This class represents a polygon in the program context. It does not represent the transporting wrapper objects.
    """
    VALID_NAME: str = "^[a-zA-Z0-9_ ]+$"

    def __init__(self, polygon: PolygonRecord):
        """
        The constructor for a new polygon

        :param polygon: The polygon record where the construction is based on
        """
        self.__corners: Optional[List[PositionRecord]] = None
        self._uuid: Optional[UUID] = None
        self.__name: Optional[str] = None
        self._error: Optional[ErrorMessage] = None
        self.set_attributes(polygon)

    def set_attributes(self, polygon: PolygonRecord) -> None:
        """
        Sets the polygon attributes based in the polygon record

        :param polygon: The polygon record
        """
        if len(polygon.corners) < 3:
            self._error = ErrorMessage.POLYGON_TOO_FEW_POINTS
            return
        if not all(-90 < corner.latitude < 90 and -180 < corner.longitude < 180 for corner in polygon.corners):
            self._error = ErrorMessage.POLYGON_ILLEGAL_COORDINATES
            return
        if re.fullmatch(pattern=self.VALID_NAME, string=polygon.name) is None:
            self._error = ErrorMessage.INVALID_NAME
            return

        self.__corners = list(polygon.corners)
        self.__name = polygon.name
        self._uuid = uuid.uuid4()

    @property
    def _corners(self) -> List[PositionRecord]:
        """
        Getter for the corners of the polygon

        :return: List of corner positions
        """
        if self.__corners is None:
            raise ExecutionFlowError(INVALID_EXECUTION_MSG)
        return self.__corners

    @property
    def _name(self):
        """
        Getter for the name of the polygon

        :return: name of the polygon
        """
        if self.__corners is None:
            raise ExecutionFlowError(INVALID_EXECUTION_MSG)
        return self.__name

    def create_polygon_record(self) -> PolygonRecord:
        """
        Returns the included data transformed in Polygon record

        :return: The Data in polygon record
        """
        corner_tuple = tuple(self._corners)
        return PolygonRecord(corner_tuple, self._name, )

    def get_corners(self) -> [PositionRecord]:
        """
        Returns all corners of the polygon

        :return: list of all corner position
        """
        return self._corners

    def get_id(self) -> Optional[UUID]:
        """
        Returns the uuid of the polygon

        :return: The uuid of the polygon
        """
        return self._uuid

    def get_error(self) -> ErrorMessage:
        """
        Getter for the latest Error message

        :return: the Message of the error
        """
        return self._error
