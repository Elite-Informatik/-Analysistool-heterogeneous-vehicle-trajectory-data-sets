from dataclasses import dataclass
from uuid import UUID

from src.controller.output_handling.abstract_event import Event


@dataclass(frozen=True)
class AnalysisChanged(Event):
    """
    Event is thrown if an analysis is edited successfully.
    """
    _id: UUID

    @property
    def id(self) -> UUID:
        """
        Returns the ID of the edited analysis

        :return: ID of the edited analysis
        """
        return self._id
