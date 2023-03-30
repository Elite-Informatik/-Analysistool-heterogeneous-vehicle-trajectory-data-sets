from dataclasses import dataclass
from uuid import UUID

from src.controller.output_handling.abstract_event import Event


@dataclass(frozen=True)
class FilterAdded(Event):
    """
    Event is thrown when a new filters is added to a filtergroup.
    """
    _id: UUID
    _group_id: UUID

    @property
    def id(self) -> UUID:
        """
        Returns the ID of the filters.

        :return: ID of the filters
        """
        return self._id

    @property
    def group_id(self) -> UUID:
        """
        Returns the ID of the parent filtergroup.

        :return: ID of the parent filtergroup
        """
        return self._group_id
