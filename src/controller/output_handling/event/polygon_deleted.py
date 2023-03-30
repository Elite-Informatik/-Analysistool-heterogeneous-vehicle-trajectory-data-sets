from dataclasses import dataclass
from uuid import UUID

from src.controller.output_handling.abstract_event import Event


@dataclass(frozen=True)
class PolygonDeleted(Event):
    """
    Event is thrown when a polygon is deleted.
    """
    _id: UUID

    @property
    def id(self) -> UUID:
        """
        Returns the ID of the deleted polygon.

        :return: ID of the deleted polygon
        """
        return self._id
