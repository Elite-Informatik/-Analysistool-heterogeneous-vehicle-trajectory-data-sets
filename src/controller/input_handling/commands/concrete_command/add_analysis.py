from src.controller.execution_handling.analysis_manager import IAnalysisManager
from src.controller.input_handling.commands.command import Command
from src.data_transfer.record import (AnalysisTypeRecord)


class AddAnalysisCommand(Command):
    """
    represents a command to add a new
    """

    def __init__(self, analysis_manager: IAnalysisManager,
                 analysis_type: AnalysisTypeRecord):
        """
        creates a new AddAnalysisCommand
        :param analysis_manager:    the analysis manager
        :param analysis_type:       the analysis type
        """
        super().__init__()
        self._analysis_manager = analysis_manager
        self._analysis_type = analysis_type

    def execute(self):
        """
        adds the new analysis
        """
        self._was_successful = self._analysis_manager.add_analysis(self._analysis_type)
