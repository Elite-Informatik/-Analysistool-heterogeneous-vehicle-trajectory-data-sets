from dataclasses import dataclass
from uuid import UUID

from src.controller.output_handling.abstract_event import Event


@dataclass(frozen=True)
class PolygonAdded(Event):
    """
    Event is thrown when a new polygon is added.
    """
    _id: UUID

    @property
    def id(self) -> UUID:
        """
        Returns the ID of the added polygon.

        :return: ID of the added polygon
        """
        return self._id
