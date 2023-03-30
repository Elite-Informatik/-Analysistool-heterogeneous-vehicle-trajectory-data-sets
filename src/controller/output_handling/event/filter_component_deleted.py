from dataclasses import dataclass
from uuid import UUID

from src.controller.output_handling.abstract_event import Event


@dataclass(frozen=True)
class FilterComponentDeleted(Event):
    """
    Event is thrown when a filters component is deleted.
    """
    _id: UUID

    @property
    def id(self) -> UUID:
        """
        Returns the ID of the deleted filters component.

        :return: ID of the deleted filters component
        """
        return self._id
