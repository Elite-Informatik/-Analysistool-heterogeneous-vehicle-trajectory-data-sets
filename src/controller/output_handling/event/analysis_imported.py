from dataclasses import dataclass

from src.controller.output_handling.abstract_event import Event
from src.data_transfer.record import AnalysisTypeRecord


@dataclass(frozen=True)
class AnalysisImported(Event):
    """
    Event is thrown if an analysis is imported successfully.
    """
    _analysis_type: AnalysisTypeRecord

    @property
    def analysis_type_id(self) -> AnalysisTypeRecord:
        """
        Returns the ID of the imported analysis

        :return: ID of the imported analysis
        """
        return self._analysis_type
