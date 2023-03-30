from dataclasses import dataclass
from uuid import UUID

from src.controller.output_handling.abstract_event import Event


@dataclass(frozen=True)
class AnalysisRefreshed(Event):
    """
    Event is thrown if an analysis is refreshed.
    """
    _id: UUID

    @property
    def id(self) -> UUID:
        """
        Returns the ID of the refreshed analysis

        :return: ID of the refreshed analysis
        """
        return self._id
