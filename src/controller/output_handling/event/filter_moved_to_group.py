from dataclasses import dataclass
from uuid import UUID

from src.controller.output_handling.abstract_event import Event


@dataclass(frozen=True)
class FilterMovedToGroup(Event):
    """
    Event is thrown when a filter is moved to a filtergroup.
    """
    _id: UUID
    _group_id: UUID

    @property
    def id(self) -> UUID:
        """
        Returns the ID of the filters component.

        :return: ID of the filters component
        """
        return self._id

    @property
    def group_id(self) -> UUID:
        """
        Returns the ID of the filtergroup.

        :return: ID of the filtergroup
        """
        return self._group_id
