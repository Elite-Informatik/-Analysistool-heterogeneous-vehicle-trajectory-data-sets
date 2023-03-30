from dataclasses import dataclass
from uuid import UUID

from src.controller.output_handling.abstract_event import Event


@dataclass(frozen=True)
class AnalysisAdded(Event):
    """
    Event is thrown when a Analysis is added successfully.
    """
    _id: UUID

    @property
    def id(self) -> UUID:
        """
        Returns the ID of the added analysis

        :return: ID of the added analysis
        """
        return self._id
