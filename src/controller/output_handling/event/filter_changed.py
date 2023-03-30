from dataclasses import dataclass
from uuid import UUID

from src.controller.output_handling.abstract_event import Event


@dataclass(frozen=True)
class FilterChanged(Event):
    """
    Event is thrown when a filters is modified.
    """
    _id: UUID

    @property
    def id(self) -> UUID:
        """
        Returns the ID of the modified filters.

        :return: ID of the modified filters
        """
        return self._id
