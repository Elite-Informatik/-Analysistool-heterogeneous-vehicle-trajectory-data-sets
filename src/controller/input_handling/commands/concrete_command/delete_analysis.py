from uuid import UUID

from src.controller.execution_handling.analysis_manager import IAnalysisManager
from src.controller.input_handling.commands.command import Command


class DeleteAnalysisCommand(Command):
    """
    represents a command to delete an analysis
    """

    def __init__(self, analysis_manager: IAnalysisManager, analysis_id: UUID):
        """
        creates a new DeleteAnalysisCommand
        :param analysis_manager:    the analysis manager
        :param analysis_id:         the id of the analysis to delete
        """
        super().__init__()
        self._analysis_manager = analysis_manager
        self._analysis_id = analysis_id

    def execute(self):
        """
        deletes the analysis with the given id
        """
        self._was_successful = self._analysis_manager.delete_analysis(self._analysis_id)
