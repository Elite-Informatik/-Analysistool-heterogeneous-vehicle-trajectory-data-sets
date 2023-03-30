from dataclasses import dataclass
from uuid import UUID

from src.controller.output_handling.abstract_event import Event


@dataclass(frozen=True)
class DatasetAdded(Event):
    """
    Event is thrown if a new dataset is added successfully.
    """
    _id: UUID

    @property
    def id(self) -> UUID:
        """
        Returns the ID of the added dataset

        :return: ID of the added dataset
        """
        return self._id
