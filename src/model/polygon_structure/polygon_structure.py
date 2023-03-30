from typing import List
from typing import Optional
from uuid import UUID

from src.data_transfer.exception import InvalidUUID
from src.data_transfer.record import PolygonRecord
from src.model.error_handler import ErrorHandler
from src.model.error_handler import ErrorMessage
from src.model.filter_structure.ifilter_structure import IFilterStructure
from src.model.polygon_structure.ipolygon_structure import IPolygonStructure
from src.model.polygon_structure.polygon import Polygon

INVALID_UUID_MSG = "Invalid UUID"
OBJECT_USE_MSG = "Object in Use"


class PolygonStructure(IPolygonStructure, ErrorHandler):
    """
    This class hosts all polygons in the model layer. It controls the manipulating of these and checks these
    manipulations looking at the connections to other moduls
    """

    def __init__(self):
        """
        Constructor for a new polygon structure.
        Setting the filter facade afterwards is necessary
        """
        super().__init__()
        self._polygons: List[Polygon] = []
        self._deleted_polygons: List[Polygon] = []
        self._filter_facade = None

    def set_filter_facade(self, filter_facade: IFilterStructure) -> None:
        """
        Setter for the filter facade

        :param filter_facade: the filter facade to set
        """
        self._filter_facade = filter_facade

    def add_polygon(self, polygon_record: PolygonRecord) -> Optional[UUID]:
        """
        Takes a polygon record and creates a Polygon from it. If one or more of the arguments are not valid the IDRecord
        will not contain a valid id as
        :param polygon_record:
        :return:
        """
        new_polygon: Polygon = Polygon(polygon_record)
        if new_polygon is None:
            self.throw_error(ErrorMessage.POLYGON_NOT_CREATED_FROM_RECORD)
            return None
        polygon_id = new_polygon.get_id()
        if polygon_id is None:
            self.throw_error(new_polygon.get_error())
            return None
        self._polygons.append(new_polygon)
        return polygon_id

    def delete_polygon(self, uuid: UUID) -> bool:
        """
        Deletes a polygon that fits the uuid
        Only executable if the uuid is not none, is used and is not used in the filter facade

        :param uuid: The uuid of the polygon to delete
        :return: if the polygon was deleted
        """
        if uuid is None:
            self.throw_error(ErrorMessage.INPUT_NONE)

        if self._filter_facade.is_polygon_in_use(uuid):
            self.throw_error(ErrorMessage.POLYGON_IN_USE)
            return False

        for polygon in self._polygons:
            if polygon.get_id() == uuid:
                self._polygons.remove(polygon)
                self._deleted_polygons.append(polygon)
                return True

        raise InvalidUUID(ErrorMessage.POLYGON_NOT_EXISTING.value)

    def get_polygon(self, polygon_id: UUID) -> PolygonRecord:
        """
        Getter for a polygon given a uuid. Is returned as polygon record to ensure
        encapsulation.

        :param polygon_id: the uuid to get
        """
        if polygon_id is None:
            raise InvalidUUID(ErrorMessage.INPUT_NONE.value)

        for polygon in self._polygons:
            if polygon.get_id() == polygon_id:
                polygon_record = polygon.create_polygon_record()
                if polygon_record is None:
                    self.throw_error(polygon.get_error())
                return polygon_record

        raise InvalidUUID(ErrorMessage.POLYGON_NOT_EXISTING.value)

    def get_all_polygon_ids(self) -> List[UUID]:
        """
        Getter for all used polygons given as uuids

        :return: List of all used uuids
        """
        return [polygon.get_id() for polygon in self._polygons]

    def get_all_polygons(self) -> List[PolygonRecord]:
        """
        Getter for all used polygons as PolygonRecords

        :return: List of used polygons
        """
        polygon_records = list()
        for polygon in self._polygons:
            polygon_records.append(polygon.create_polygon_record())
        return polygon_records

    def reconstruct_polygon(self) -> Optional[UUID]:
        """
        Reconstructs a polygon. THe uuid is returned to identify the reconstructed polygon

        :return: uuid of the reconstructed polygoin
        """
        if len(self._deleted_polygons) <= 0:
            self.throw_error(ErrorMessage.NO_POLYGON_DELETED)
            return None

        reconstructed: Polygon = self._deleted_polygons.pop()
        self._polygons.append(reconstructed)
        return reconstructed.get_id()

    def remove_latest_polygon(self) -> Optional[UUID]:
        """
        Remove the polygon added the latest

        :return: the UUID of the polygon removed
        """
        if len(self._polygons) <= 0:
            self.throw_error(ErrorMessage.NO_POLYGON_ADDED)
            return None

        return self._polygons.pop().get_id()

    def is_polygon_in_use(self, uuid) -> bool:
        """
        Checks, if a polygon is used in the model based on a given uuid

        :param uuid: the uuid of the polygon to check
        """
        if uuid is None:
            self.throw_error(ErrorMessage.INPUT_NONE)
            return False
        return uuid in [polygon.get_id() for polygon in self._polygons]
