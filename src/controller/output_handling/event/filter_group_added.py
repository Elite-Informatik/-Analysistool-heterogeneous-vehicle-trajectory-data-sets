from dataclasses import dataclass
from uuid import UUID

from src.controller.output_handling.abstract_event import Event


@dataclass(frozen=True)
class FilterGroupAdded(Event):
    """
    Event is thrown when a new filters group is added.
    """
    _id: UUID
    _group_id: UUID

    @property
    def id(self) -> UUID:
        """
        Returns the ID of the added filters group.

        :return: ID of the added filters group
        """
        return self._id

    @property
    def group_id(self) -> UUID:
        """
        Returns the ID of the parent filters group.

        :return: ID of the parent filters group
        """
        return self._group_id
