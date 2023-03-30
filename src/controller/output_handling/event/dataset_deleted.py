from dataclasses import dataclass
from uuid import UUID

from src.controller.output_handling.abstract_event import Event


@dataclass(frozen=True)
class DatasetDeleted(Event):
    """
    Event is thrown if a new dataset is deleted successfully.
    """
    _id: UUID

    @property
    def id(self) -> UUID:
        """
        Returns the ID of the deleted dataset

        :return: ID of the deleted dataset
        """
        return self._id
