from abc import ABC
from abc import abstractmethod
from typing import Optional
from uuid import UUID

from src.data_transfer.exception import InvalidUUID
from src.controller.execution_handling.abstract_manager import AbstractManager
from src.controller.facade_consumer.polygon_facade_consumer import PolygonFacadeConsumer
from src.controller.output_handling.event import PolygonAdded
from src.controller.output_handling.event import PolygonDeleted
from src.data_transfer.content import type_check
from src.data_transfer.record import PolygonRecord


class IPolygonManager(ABC):
    """
    This Manager is responsible for manipulating the polygon structures.
    """

    @abstractmethod
    def add_polygon(self, polygon_record: PolygonRecord) -> Optional[UUID]:
        """
        This method adds a polygon Record to the model layer.

        :param polygon_record: the polygon to add

        :return: the new polygon id
        """

        pass

    @abstractmethod
    def delete_polygon(self, uuid: UUID) -> bool:
        """
        This method deletes a polygon from the model layer

        :param uuid: The polygon to delete

        :return: True if the polygon was deleted, False otherwise
        """
        pass

    @abstractmethod
    def undo_deletion(self) -> bool:
        """
        Undoes the last polygon removal if possible

        :return: Addedpolygon event if possible
        """

    @abstractmethod
    def undo_addition(self) -> bool:
        """
        Undos the last polygon addition if possible

        :return: DeletedPolygon event if possible
        """


class IPolygonGetter(ABC):
    """
    This interface encapsulates all getter-methods of a polygon manager
    """

    @abstractmethod
    def get_polygon(self, uuid: UUID) -> PolygonRecord:
        """
        Gets the corresponding polygon to a uuid

        :param uuid: The uuid

        :return: The polygon record
        """
        pass

    def get_polygon_ids(self) -> [UUID]:
        """
        gets the ids of all polygons
        :return: all polygon ids
        """
        pass


class PolygonManager(IPolygonGetter, IPolygonManager, PolygonFacadeConsumer, AbstractManager):
    """
    This class implements the PolygonManager Interface. It makes use of the model facade.
    """

    def __init__(self):
        IPolygonGetter.__init__(self)
        IPolygonManager.__init__(self)
        PolygonFacadeConsumer.__init__(self)
        AbstractManager.__init__(self)

    @type_check(PolygonRecord)
    def add_polygon(self, polygon_record: PolygonRecord) -> Optional[UUID]:

        uuid = self.polygon_facade.add_polygon(polygon_record)
        if uuid is None:
            self.handle_error([self.polygon_facade])
            return None

        self.events.extend([PolygonAdded(uuid)])
        self.handle_event()
        return uuid

    @type_check(UUID)
    def delete_polygon(self, uuid: UUID) -> bool:

        if not self.polygon_facade.delete_polygon(uuid):
            self.handle_error([self.polygon_facade])
            return False
        self.events.extend([PolygonDeleted(uuid)])
        self.handle_event()
        return True

    def undo_deletion(self):
        returned_uuid = self.polygon_facade.reconstruct_polygon()
        if returned_uuid is None:
            self.handle_error([self.polygon_facade])
            return
        self.events.extend([PolygonAdded(returned_uuid)])
        self.handle_event()

    def undo_addition(self):
        returned_uuid = self.polygon_facade.remove_latest_polygon()
        if returned_uuid is None:
            self.handle_error([self.polygon_facade])
            return
        self.events.extend([PolygonDeleted(returned_uuid)])
        self.handle_event()

    @type_check(UUID)
    def get_polygon(self, polygon_id: UUID) -> Optional[PolygonRecord]:
        return self.polygon_facade.get_polygon(polygon_id)

    def get_polygon_ids(self) -> [UUID]:
        return self.polygon_facade.get_all_polygon_ids()
