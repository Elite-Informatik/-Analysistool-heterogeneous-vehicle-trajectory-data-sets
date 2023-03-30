from dataclasses import dataclass
from uuid import UUID

from src.controller.output_handling.abstract_event import Event


@dataclass(frozen=True)
class FilterGroupChanged(Event):
    """
    Event is thrown when a filters group is changed.
    """
    _id: UUID

    @property
    def id(self) -> UUID:
        """
        Returns the ID of the changed filters group.

        :return: ID of the changed filters group
        """
        return self._id
