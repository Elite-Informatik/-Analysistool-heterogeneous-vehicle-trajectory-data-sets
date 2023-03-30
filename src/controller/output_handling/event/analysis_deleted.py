from dataclasses import dataclass
from uuid import UUID

from src.controller.output_handling.abstract_event import Event


@dataclass(frozen=True)
class AnalysisDeleted(Event):
    """
    Event is thrown if an analysis is deleted successfully.
    """
    _id: UUID

    @property
    def id(self) -> UUID:
        """
        Returns the ID of the deleted analysis

        :return: ID of the deleted analysis
        """
        return self._id
