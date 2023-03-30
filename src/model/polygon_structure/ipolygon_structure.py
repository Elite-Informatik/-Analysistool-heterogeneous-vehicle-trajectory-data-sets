from abc import abstractmethod
from typing import List
from typing import Optional
from uuid import UUID

from src.data_transfer.record.polygon_record import PolygonRecord


class IPolygonStructure:
    """
    This interface is the facade for the polygon structure. It allows manipulating the included polygons.
    """

    @abstractmethod
    def add_polygon(self, polygon: PolygonRecord) -> Optional[UUID]:
        """
        This method adds a polygon to the polygon structure based on an polygon record

        :param polygon: The polygon to add

        :return: The resulting UUID
        """

        pass

    @abstractmethod
    def delete_polygon(self, uuid: UUID) -> bool:
        """
        This method deletes a polygon based on the given uuid.

        :param uuid: The uuid from which the polygon should be deleted

        :return: boolean if the deletion was successful
        """

        pass

    @abstractmethod
    def get_polygon(self, uuid: UUID) -> Optional[PolygonRecord]:
        """
        This method gets a copy of polygon to a given uuid

        :param uuid: The corresponding uuid

        :return: the polygon copy in a PolygonRecord
        """

        pass

    @abstractmethod
    def get_all_polygon_ids(self) -> List[UUID]:
        """
        This method returns all uuids that are connected to polygon

        :return: The list of all polygon uuids
        """

        pass

    @abstractmethod
    def get_all_polygons(self) -> List[PolygonRecord]:
        """
        This methods returns a list of copies of all polygons

        :return: PolygonRecord list with all polygon copies
        """

        pass

    @abstractmethod
    def reconstruct_polygon(self) -> Optional[UUID]:
        """
        This method reconstructs the last polygon deleted. If no polygon was deleted it returns false, if the
        reconstruction was successful it returns true

        :return: If the reconstruction was successful, then uuid
        """

        pass

    @abstractmethod
    def remove_latest_polygon(self) -> Optional[UUID]:
        """
        This method removes the polygon which was added at last. It DOES NOT add the polygon to the removal stack

        :return: if the removal was successful, then uuid
        """

        pass
