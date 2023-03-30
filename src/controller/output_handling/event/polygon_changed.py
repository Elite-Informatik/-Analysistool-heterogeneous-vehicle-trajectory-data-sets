from dataclasses import dataclass
from uuid import UUID

from src.controller.output_handling.abstract_event import Event


@dataclass(frozen=True)
class PolygonChanged(Event):
    """
    Event is thrown when a polygon is changed.
    """
    _id: UUID

    @property
    def id(self) -> UUID:
        """
        Returns the ID of the changed polygon.

        :return: ID of the changed polygon
        """
        return self._id
